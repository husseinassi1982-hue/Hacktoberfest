import os
import tempfile

_database = tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False)
_database.close()
os.environ["APP_DATABASE_PATH"] = _database.name

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def auth_headers() -> dict[str, str]:
    email = "integration@example.com"
    response = client.post("/auth/register", json={"email": email, "password": "password123"})
    if response.status_code == 409:
        response = client.post("/auth/login", json={"email": email, "password": "password123"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['token']}"}


def test_profile_and_portfolio_are_scoped_to_authenticated_user():
    headers = auth_headers()
    profile = {
        "annual_income": 80000,
        "liquid_savings": 25000,
        "debts": 5000,
        "amount_to_invest": 10000,
        "monthly_contribution": 500,
        "investment_horizon_years": 10,
        "risk_tolerance": 3,
        "risk_capacity": 3,
        "investment_goal": "Retraite",
        "constraints": "",
    }
    saved = client.post("/profile/", json=profile, headers=headers)
    assert saved.status_code == 200
    assert client.get("/profile/", headers=headers).json()["profile"]["investment_goal"] == "Retraite"

    portfolio = client.post("/portfolio/saved", headers=headers, json={
        "name": "Long terme",
        "portfolio": {"cash": 1000, "positions": [{"symbol": "ETF", "quantity": 2, "price": 100, "sector": "Global", "asset_type": "equity_etf"}]},
    })
    assert portfolio.status_code == 200
    assert len(client.get("/portfolio/saved", headers=headers).json()["portfolios"]) == 1

    advisor = client.post("/agent/chat", headers=headers, json={"message": "Quel est le risque de mon portefeuille ?"})
    assert advisor.status_code == 200
    assert {tool["name"] for tool in advisor.json()["tools_used"]} >= {"analyze_portfolio", "stress_test"}


def test_agent_requires_authentication():
    assert client.post("/agent/chat", json={"message": "Bonjour"}).status_code == 401


def test_rag_ingestion_returns_ranked_sources():
    headers = auth_headers()
    created = client.post("/rag/documents", headers=headers, json={
        "title": "Banque centrale",
        "content": "La banque centrale maintient son taux directeur pour lutter contre l’inflation.",
        "publisher": "Source officielle",
        "reliability": 1,
    })
    assert created.status_code == 200
    results = client.get("/rag/search", headers=headers, params={"query": "taux directeur inflation"})
    assert results.status_code == 200
    assert results.json()["sources"][0]["title"] == "Banque centrale"

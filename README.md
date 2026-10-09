# Portfolio Advisor

Project scaffold for a portfolio analytics and AI advisor application.

## Structure

```text
backend/app/api/portfolio.py
backend/app/api/market.py
backend/app/api/agent.py
backend/app/api/profile.py
backend/app/agent/gemma.py
backend/app/agent/tools.py
backend/app/agent/prompts.py
backend/app/quant/portfolio.py
backend/app/quant/risk.py
backend/app/quant/optimizer.py
backend/app/quant/monte_carlo.py
backend/app/quant/backtest.py
backend/app/quant/scenarios.py
backend/app/data/market.py
backend/app/data/macro.py
backend/app/data/news.py
backend/app/rag/ingest.py
backend/app/rag/embeddings.py
backend/app/rag/retrieval.py
backend/app/services/suitability.py
backend/app/services/charts.py
backend/app/main.py
backend/app/models/.gitkeep
backend/app/database/.gitkeep
backend/requirements.txt
frontend/src/pages/Dashboard.tsx
frontend/src/pages/Portfolio.tsx
frontend/src/pages/Advisor.tsx
frontend/src/pages/Profile.tsx
frontend/src/components/PortfolioValue.tsx
frontend/src/components/AllocationChart.tsx
frontend/src/components/RiskCard.tsx
frontend/src/components/MonteCarloChart.tsx
frontend/src/components/AgentChat.tsx
```

The backend is organized into API, agent, quantitative analytics, data, RAG, services, models, and database modules. The frontend contains React TypeScript page and component placeholders.

## Status

This change establishes the requested structure. Financial calculations, market providers, Gemma, RAG, persistence, and UI behavior remain unimplemented. The frontend is source scaffolding; its package configuration, entry point, and build tooling still need to be added. Empty models and database directories are tracked with .gitkeep files.

## Backend development

Requires Python 3.10+.

```sh
cd backend
python -m venv .venv
```

Activate the environment, then run:

```sh
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health endpoint: http://localhost:8000/health. API documentation: http://localhost:8000/docs.

from fastapi import FastAPI

from app.api.profile import router as profile_router
from app.api.portfolio import router as portfolio_router
from app.api.market import router as market_router


app = FastAPI(
    title="FinPilot AI",
    description="AI-powered portfolio intelligence platform",
    version="0.1.0"
)


app.include_router(profile_router)
app.include_router(portfolio_router)
app.include_router(market_router)


@app.get("/")
def root():
    return {
        "message": "FinPilot AI API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
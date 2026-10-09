import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.profile import router as profile_router
from app.api.portfolio import router as portfolio_router
from app.api.market import router as market_router
from app.api.agent import router as agent_router
from app.api.auth import router as auth_router
from app.database.auth import initialize_auth_database


app = FastAPI(
    title="FinPilot AI",
    description="AI-powered portfolio intelligence platform",
    version="0.1.0"
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://127.0.0.1:5173,http://localhost:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValueError)
async def value_error_handler(_: Request, error: ValueError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(error)})


app.include_router(profile_router)
app.include_router(portfolio_router)
app.include_router(market_router)
app.include_router(agent_router)
app.include_router(auth_router)
initialize_auth_database()


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
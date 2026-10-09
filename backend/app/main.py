from fastapi import FastAPI
from app.api.profile import router as profile_router

app = FastAPI(
    title = "FinPilot AI",
    description = "AI-powered portfolio",
    version = "0.1.0"
)

app.include_router(profile_router)

@app.get("/")
def root():
    return {
        "message" : "FinPilot AI API"
    }

@app.get("/health")
def health():
    return {
        "status" : "ok"
    }
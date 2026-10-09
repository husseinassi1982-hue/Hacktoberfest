"""Backend entry point."""
from fastapi import FastAPI

app = FastAPI(title="Portfolio Advisor")

@app.get("/health")
def health():
    return {"status": "ok", "implementation": "scaffold"}

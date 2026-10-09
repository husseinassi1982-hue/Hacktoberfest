from pydantic import BaseModel

class BacktestRequest(BaseModel):
    symbols: list [str]
    weights: list[float]

    period: str = "5y"
    benchmark: str = "SPY"

    risk_free_rate: float = 0.03
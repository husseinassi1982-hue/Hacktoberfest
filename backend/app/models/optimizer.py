from pydantic import BaseModel, Field
from app.models.profile import InvestorProfile


class OptimizerRequest(BaseModel):
    symbols: list[str]

    expected_returns: list[float]

    covariance_matrix: list[list[float]]

    objective: str = "maximize_sharpe"

    risk_free_rate: float = 0.03

    max_weight: float = Field(
        default=1.0,
        gt=0,
        le=1
    )

class AutoOptimizerRequest(BaseModel):
    symbols: list[str]

    period: str = "1y"

    objective: str = "maximize_sharpe"

    risk_free_rate: float = 0.03

    max_weight: float = Field(
        default=1.0,
        gt=0,
        le=1
    )

class ProfileOptimizerRequest(BaseModel):
    profile: InvestorProfile

    symbols: list[str]
    asset_types: list[str]
    sectors: list[str]

    period: str = "1y"
    objective: str = "maximize_sharpe"
    risk_free_rate: float = 0.03
from pydantic import BaseModel, Field


class MonteCarloRequest(BaseModel):
    starting_value: float = Field(gt=0)

    monthly_contribution: float = Field(
        default=0,
        ge=0
    )

    years: int = Field(
        gt=0,
        le=50
    )

    expected_annual_return: float

    annual_volatility: float = Field(
        ge=0
    )

    simulations: int = Field(
        default=10000,
        ge=100,
        le=50000
    )

    target_value: float | None = Field(
        default=None,
        gt=0
    )
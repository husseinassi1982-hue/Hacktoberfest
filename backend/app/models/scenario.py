from pydantic import BaseModel, Field, field_validator

from app.models.portfolio import Portfolio


class ScenarioInput(BaseModel):
    name: str = "custom"
    equity_shock: float = Field(default=0.0, ge=-1.0, le=1.0)
    bond_shock: float = Field(default=0.0, ge=-1.0, le=1.0)
    sector_shocks: dict[str, float] = Field(default_factory=dict)
    symbol_shocks: dict[str, float] = Field(default_factory=dict)

    @field_validator("sector_shocks", "symbol_shocks")
    @classmethod
    def validate_shocks(cls, shocks: dict[str, float]) -> dict[str, float]:
        for key, value in shocks.items():
            if not -1.0 <= value <= 1.0:
                raise ValueError(f"Shock for {key} must be between -1.0 and 1.0.")
        return shocks


class StressTestRequest(BaseModel):
    portfolio: Portfolio
    scenario: ScenarioInput

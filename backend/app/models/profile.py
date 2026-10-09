from pydantic import BaseModel, Field
from typing import List


class InvestorProfile(BaseModel):
    annual_income: float = Field(gt=0)
    liquid_savings: float = Field(ge=0)
    debts: float = Field(ge=0)

    amount_to_invest: float = Field(gt=0)
    monthly_contribution: float = Field(ge=0)

    investment_horizon_years: int = Field(gt=0)

    risk_tolerance: int = Field(ge=1, le=5)
    risk_capacity: int = Field(ge=1, le=5)

    investment_goal: str

    preferred_assets: List[str] = []
    preferred_sectors: List[str] = []
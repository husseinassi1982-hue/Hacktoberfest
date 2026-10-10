from pydantic import BaseModel, Field, field_validator
from typing import List


class InvestorProfile(BaseModel):
    display_name: str | None = None
    tax_residence: str | None = None
    currency: str = "CAD"
    annual_income: float = Field(gt=0)
    liquid_savings: float = Field(ge=0)
    debts: float = Field(ge=0)

    amount_to_invest: float = Field(gt=0)
    monthly_contribution: float = Field(ge=0)

    investment_horizon_years: int = Field(gt=0)

    risk_tolerance: int = Field(ge=1, le=5)
    risk_capacity: int = Field(ge=1, le=5)
    max_loss_percent: float | None = Field(default=None, ge=0, le=100)

    investment_goal: str

    preferred_assets: List[str] = Field(default_factory=list)
    preferred_sectors: List[str] = Field(default_factory=list)

    age: int | None = Field(default=None, ge=18, le=120)
    family_situation: str | None = None
    dependents: int = Field(default=0, ge=0)
    profession: str | None = None
    income_stability: str | None = None
    net_worth: float | None = Field(default=None, ge=0)
    real_estate_assets: float | None = Field(default=None, ge=0)
    monthly_expenses: float | None = Field(default=None, ge=0)
    liquidity_needs: str | None = None
    emergency_fund: float | None = Field(default=None, ge=0)
    investment_experience: str | None = None
    products_used: List[str] = Field(default_factory=list)
    financial_knowledge: str | None = None
    tax_considerations: str | None = None
    financial_goal_amount: float | None = Field(default=None, ge=0)
    target_date: str | None = None
    constraints: List[str] = Field(default_factory=list)
    exclusions: List[str] = Field(default_factory=list)
    esg_preferences: List[str] = Field(default_factory=list)
    calculated_risk_profile: int | None = Field(default=None, ge=1, le=5)

    @field_validator("constraints", mode="before")
    @classmethod
    def normalize_constraints(cls, value):
        """Accept the legacy text value while the frontend is being upgraded."""
        if value is None:
            return []
        if isinstance(value, str):
            return [value.strip()] if value.strip() else []
        return value

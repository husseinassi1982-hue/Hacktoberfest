from pydantic import BaseModel

from app.models.profile import InvestorProfile
from app.models.portfolio import Portfolio


class SuitabilityRequest(BaseModel):
    profile: InvestorProfile
    portfolio: Portfolio
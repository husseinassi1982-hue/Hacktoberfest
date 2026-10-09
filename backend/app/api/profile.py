from fastapi import APIRouter

from app.models.profile import InvestorProfile
from app.services.suitability import get_risk_profile

router = APIRouter(
    prefix = "/profile",
    tags=["Investor Profile"]
)

@router.post("/")
def create_profile(profile: InvestorProfile):

   risk_profile = get_risk_profile(profile)

   return {
      "profile" : profile,
      "risk_profile" : risk_profile
   }

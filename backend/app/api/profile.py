from fastapi import APIRouter

from app.models.profile import InvestorProfile

router = APIRouter(
    prefix = "/profile",
    tags=["Investor Profile"]
)

@router.post("/")
def create_profile(profile: InvestorProfile):

    effective_risk = min(
        profile.risk_tolerance,
        profile.risk_capacity
    )

    return {
        "profile" : profile,
        "effective" : effective_risk
    }

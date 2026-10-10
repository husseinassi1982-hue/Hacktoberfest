from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user
from app.database.persistence import get_profile, save_profile
from app.models.profile import InvestorProfile
from app.services.suitability import get_risk_profile

router = APIRouter(
    prefix = "/profile",
    tags=["Investor Profile"]
)

@router.get("/")
def read_profile(user: dict[str, str] = Depends(get_current_user)):
   stored = get_profile(int(user["id"]))
   return stored or {"profile": None, "risk_profile": None}


@router.post("/")
def create_profile(
   profile: InvestorProfile,
   user: dict[str, str] = Depends(get_current_user),
):

   risk_profile = get_risk_profile(profile)

   return save_profile(int(user["id"]), profile, risk_profile)

from app.models.profile import InvestorProfile
from app.models.portfolio import Portfolio
from app.quant.portfolio import analyze_portfolio


RISK_PROFILES = {
    1: {
        "label": "very_conservative",
        "max_equity": 0.30,
        "min_bonds": 0.50,
        "max_sector": 0.20,
        "max_single_asset": 0.05,
    },
    2: {
        "label": "conservative",
        "max_equity": 0.50,
        "min_bonds": 0.30,
        "max_sector": 0.25,
        "max_single_asset": 0.10,
    },
    3: {
        "label": "moderate",
        "max_equity": 0.75,
        "min_bonds": 0.15,
        "max_sector": 0.35,
        "max_single_asset": 0.15,
    },
    4: {
        "label": "growth",
        "max_equity": 0.90,
        "min_bonds": 0.05,
        "max_sector": 0.45,
        "max_single_asset": 0.20,
    },
    5: {
        "label": "aggressive",
        "max_equity": 1.00,
        "min_bonds": 0.00,
        "max_sector": 0.60,
        "max_single_asset": 0.25,
    },
}


def get_effective_risk(profile: InvestorProfile) -> int:
    return min(
        profile.risk_tolerance,
        profile.risk_capacity
    )


def get_risk_profile(profile: InvestorProfile) -> dict:
    effective_risk = get_effective_risk(profile)

    risk_profile = RISK_PROFILES[effective_risk]

    return {
        "score": effective_risk,
        **risk_profile
    }

def check_portfolio_suitability(
    profile: InvestorProfile,
    portfolio: Portfolio
) -> dict:

    risk_profile = get_risk_profile(profile)
    analysis = analyze_portfolio(portfolio)

    violations = []
    warnings = []

    total_value = analysis["total_value"]

    if total_value == 0:
        return {
            "suitable": False,
            "violations": ["Portfolio value is zero."]
        }

   

    for position in analysis["positions"]:

        if position["weight"] > risk_profile["max_single_asset"]:

            violations.append({
                "type": "single_asset_concentration",
                "symbol": position["symbol"],
                "current_weight": position["weight"],
                "maximum_allowed": risk_profile["max_single_asset"]
            })

  

    for sector, allocation in analysis["sector_allocation"].items():

        if allocation["weight"] > risk_profile["max_sector"]:

            violations.append({
                "type": "sector_concentration",
                "sector": sector,
                "current_weight": allocation["weight"],
                "maximum_allowed": risk_profile["max_sector"]
            })

    

    equity_value = 0
    bond_value = 0

    for position in analysis["positions"]:

        asset_type = position["asset_type"].lower()

        if asset_type in ["stock", "equity_etf"]:
            equity_value += position["market_value"]

        elif asset_type in ["bond", "bond_etf"]:
            bond_value += position["market_value"]

        else:
            warnings.append(
                f"Unknown asset type for {position['symbol']}: "
                f"{position['asset_type']}"
            )

    equity_weight = equity_value / total_value
    bond_weight = bond_value / total_value

    if equity_weight > risk_profile["max_equity"]:

        violations.append({
            "type": "equity_exposure",
            "current_weight": equity_weight,
            "maximum_allowed": risk_profile["max_equity"]
        })

    if bond_weight < risk_profile["min_bonds"]:

        violations.append({
            "type": "bond_allocation",
            "current_weight": bond_weight,
            "minimum_required": risk_profile["min_bonds"]
        })

    return {
        "suitable": len(violations) == 0,
        "risk_profile": risk_profile,
        "portfolio_metrics": {
            "total_value": total_value,
            "equity_weight": equity_weight,
            "bond_weight": bond_weight,
            "cash_weight": analysis["cash_weight"]
        },
        "violations": violations,
        "warnings": warnings
    }
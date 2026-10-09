from typing import Any

from app.models.portfolio import Portfolio


EQUITY_TYPES = {"stock", "equity", "equity_etf"}
BOND_TYPES = {"bond", "bond_etf"}

PRESET_SCENARIOS = {
    "equity_selloff_20": {
        "name": "Broad equity selloff -20%",
        "equity_shock": -0.20,
        "bond_shock": 0.0,
        "sector_shocks": {},
        "symbol_shocks": {},
    },
    "tech_selloff_30": {
        "name": "Technology sector selloff -30%",
        "equity_shock": 0.0,
        "bond_shock": 0.0,
        "sector_shocks": {"technology": -0.30},
        "symbol_shocks": {},
    },
    "bond_selloff_10": {
        "name": "Bond market selloff -10%",
        "equity_shock": 0.0,
        "bond_shock": -0.10,
        "sector_shocks": {},
        "symbol_shocks": {},
    },
    "risk_off": {
        "name": "Risk-off scenario",
        "equity_shock": -0.20,
        "bond_shock": 0.05,
        "sector_shocks": {},
        "symbol_shocks": {},
    },
}


def validate_shock(value: float, name: str) -> None:
    if not -1.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between -1.0 and 1.0.")


def validate_scenario(scenario: dict[str, Any]) -> None:
    validate_shock(scenario.get("equity_shock", 0.0), "equity_shock")
    validate_shock(scenario.get("bond_shock", 0.0), "bond_shock")

    for sector, shock in scenario.get("sector_shocks", {}).items():
        validate_shock(shock, f"sector_shock:{sector}")

    for symbol, shock in scenario.get("symbol_shocks", {}).items():
        validate_shock(shock, f"symbol_shock:{symbol}")


def run_stress_test(portfolio: Portfolio, scenario: dict[str, Any]) -> dict[str, Any]:
    validate_scenario(scenario)

    sector_shocks = {
        sector.lower(): shock
        for sector, shock in scenario.get("sector_shocks", {}).items()
    }
    symbol_shocks = {
        symbol.upper(): shock
        for symbol, shock in scenario.get("symbol_shocks", {}).items()
    }

    positions: list[dict[str, Any]] = []
    sector_summary: dict[str, dict[str, float]] = {}
    warnings: list[str] = []
    current_invested_value = 0.0
    stressed_invested_value = 0.0

    for position in portfolio.positions:
        symbol = position.symbol.upper()
        sector = position.sector.lower()
        asset_type = position.asset_type.lower()
        current_value = position.quantity * position.price
        current_invested_value += current_value

        if asset_type in EQUITY_TYPES:
            base_shock = scenario.get("equity_shock", 0.0)
        elif asset_type in BOND_TYPES:
            base_shock = scenario.get("bond_shock", 0.0)
        else:
            base_shock = 0.0
            warnings.append(
                f"No global shock rule for asset type '{asset_type}' ({symbol})."
            )

        total_shock = max(
            -1.0,
            min(
                1.0,
                base_shock
                + sector_shocks.get(sector, 0.0)
                + symbol_shocks.get(symbol, 0.0),
            ),
        )
        stressed_value = current_value * (1 + total_shock)
        pnl = stressed_value - current_value
        stressed_invested_value += stressed_value

        positions.append(
            {
                "symbol": symbol,
                "sector": sector,
                "asset_type": asset_type,
                "current_value": round(current_value, 2),
                "shock": round(total_shock, 4),
                "stressed_value": round(stressed_value, 2),
                "pnl": round(pnl, 2),
            }
        )

        summary = sector_summary.setdefault(
            sector,
            {"current_value": 0.0, "stressed_value": 0.0, "pnl": 0.0},
        )
        summary["current_value"] += current_value
        summary["stressed_value"] += stressed_value
        summary["pnl"] += pnl

    current_total_value = current_invested_value + portfolio.cash
    stressed_total_value = stressed_invested_value + portfolio.cash
    total_pnl = stressed_total_value - current_total_value

    return {
        "scenario": scenario,
        "current_portfolio_value": round(current_total_value, 2),
        "stressed_portfolio_value": round(stressed_total_value, 2),
        "total_pnl": round(total_pnl, 2),
        "portfolio_return": round(
            total_pnl / current_total_value if current_total_value > 0 else 0.0,
            4,
        ),
        "positions": positions,
        "sector_summary": {
            sector: {key: round(value, 2) for key, value in summary.items()}
            for sector, summary in sector_summary.items()
        },
        "worst_contributors": sorted(positions, key=lambda position: position["pnl"])[:5],
        "warnings": warnings,
    }


def get_preset_scenario(name: str) -> dict[str, Any]:
    key = name.lower()
    if key not in PRESET_SCENARIOS:
        raise ValueError(f"Unknown stress scenario: {name}")
    return PRESET_SCENARIOS[key]


def get_available_scenarios() -> dict[str, dict[str, Any]]:
    return PRESET_SCENARIOS

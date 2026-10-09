from typing import Any

from app.quant.portfolio import analyze_portfolio
from app.quant.scenarios import run_stress_test
from app.models.portfolio import Portfolio


def portfolio_chart_data(portfolio: Portfolio) -> dict[str, Any]:
    analysis = analyze_portfolio(portfolio)
    allocation = [
        {
            "name": sector,
            "value": details["value"],
            "weight": details["weight"],
        }
        for sector, details in analysis["sector_allocation"].items()
    ]
    if portfolio.cash:
        allocation.append(
            {
                "name": "cash",
                "value": portfolio.cash,
                "weight": analysis["cash_weight"],
            }
        )

    return {
        "charts": [
            {
                "type": "allocation",
                "title": "Portfolio allocation by sector",
                "series": allocation,
            }
        ]
    }


def stress_chart_data(portfolio: Portfolio, scenario: dict[str, Any]) -> dict[str, Any]:
    result = run_stress_test(portfolio, scenario)
    return {
        "charts": [
            {
                "type": "stress-impact",
                "title": scenario.get("name", "Stress scenario"),
                "series": [
                    {
                        "name": position["symbol"],
                        "current": position["current_value"],
                        "stressed": position["stressed_value"],
                        "pnl": position["pnl"],
                    }
                    for position in result["positions"]
                ],
            }
        ]
    }

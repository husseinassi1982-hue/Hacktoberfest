from app.models.portfolio import Portfolio
from app.quant.portfolio import analyze_portfolio
from app.quant.risk import calculate_risk_metrics
from app.quant.scenarios import get_preset_scenario, run_stress_test


def analyze_portfolio_tool(portfolio: Portfolio) -> dict:
    return analyze_portfolio(portfolio)


def stress_test_tool(portfolio: Portfolio, preset: str = "risk_off") -> dict:
    return run_stress_test(portfolio, get_preset_scenario(preset))


def risk_metrics_tool(prices: list[float]) -> dict:
    return calculate_risk_metrics(prices)

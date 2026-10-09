from fastapi import APIRouter
from app.models.portfolio import Portfolio
from app.quant.portfolio import analyze_portfolio
from app.models.suitability import SuitabilityRequest
from app.services.suitability import check_portfolio_suitability
from app.models.monte_carlo import MonteCarloRequest
from app.quant.monte_carlo import run_monte_carlo

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)


@router.post("/analyze")
def analyze(portfolio: Portfolio):

    return analyze_portfolio(portfolio)

@router.post("/suitability")
def check_suitability(request: SuitabilityRequest):

    return check_portfolio_suitability(
        request.profile,
        request.portfolio
    )

@router.post("/monte-carlo")
def monte_carlo(
    request: MonteCarloRequest
):

    return run_monte_carlo(
        starting_value=request.starting_value,
        monthly_contribution=request.monthly_contribution,
        years=request.years,
        expected_annual_return=request.expected_annual_return,
        annual_volatility=request.annual_volatility,
        simulations=request.simulations,
        target_value=request.target_value
    )
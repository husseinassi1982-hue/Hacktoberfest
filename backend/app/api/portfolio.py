from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_user
from app.database.persistence import delete_portfolio, get_portfolio, list_portfolios, save_portfolio
from app.models.portfolio import Portfolio, StoredPortfolioRequest
from app.quant.portfolio import analyze_portfolio
from app.models.suitability import SuitabilityRequest
from app.services.suitability import check_portfolio_suitability
from app.models.monte_carlo import MonteCarloRequest
from app.quant.monte_carlo import run_monte_carlo
from app.models.optimizer import OptimizerRequest
from app.quant.optimizer import optimize_portfolio
from app.models.optimizer import AutoOptimizerRequest
from app.data.market import get_multiple_close_prices
from app.models.optimizer import ProfileOptimizerRequest
from app.services.suitability import get_risk_profile
from app.quant.optimizer import (
    optimize_portfolio,
    calculate_market_statistics,
    optimize_portfolio_with_constraints
)

from app.models.backtest import BacktestRequest
from app.quant.backtest import run_backtest
from app.models.scenario import StressTestRequest
from app.quant.scenarios import (
    get_available_scenarios,
    get_preset_scenario,
    run_stress_test,
)
from app.models.charts import ChartDataRequest
from app.services.charts import portfolio_chart_data, stress_chart_data

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)


@router.get("/saved")
def saved_portfolios(user: dict[str, str] = Depends(get_current_user)):
    return {"portfolios": list_portfolios(int(user["id"]))}


@router.get("/saved/{portfolio_id}")
def saved_portfolio(portfolio_id: int, user: dict[str, str] = Depends(get_current_user)):
    result = get_portfolio(int(user["id"]), portfolio_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found.")
    return result


@router.post("/saved")
def create_saved_portfolio(request: StoredPortfolioRequest, user: dict[str, str] = Depends(get_current_user)):
    return save_portfolio(int(user["id"]), request.name, request.portfolio)


@router.delete("/saved/{portfolio_id}")
def remove_saved_portfolio(portfolio_id: int, user: dict[str, str] = Depends(get_current_user)):
    if not delete_portfolio(int(user["id"]), portfolio_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found.")
    return {"message": "Portfolio deleted."}


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

@router.post("/optimize")
def optimize(request: OptimizerRequest):

    if len(request.symbols) != len(
        request.expected_returns
    ):
        raise ValueError(
            "Symbols and expected returns "
            "must contain the same number of assets."
        )

    result = optimize_portfolio(
        expected_returns=request.expected_returns,
        covariance_matrix=request.covariance_matrix,
        objective=request.objective,
        risk_free_rate=request.risk_free_rate,
        max_weight=request.max_weight
    )

    allocations = {}

    for symbol, weight in zip(
        request.symbols,
        result["weights"]
    ):
        allocations[symbol.upper()] = weight

    return {
        "objective": request.objective,
        "allocations": allocations,
        "expected_return":
            result["expected_return"],
        "volatility":
            result["volatility"],
        "sharpe_ratio":
            result["sharpe_ratio"]
    }

@router.post("/optimize-auto")
def optimize_auto(
    request: AutoOptimizerRequest
):

    if len(request.symbols) < 2:
        raise ValueError(
            "At least two symbols are required."
        )

    prices = get_multiple_close_prices(
        request.symbols,
        request.period
    )

    expected_returns, covariance_matrix = (
        calculate_market_statistics(prices)
    )

    result = optimize_portfolio(
        expected_returns=expected_returns.tolist(),
        covariance_matrix=covariance_matrix.tolist(),
        objective=request.objective,
        risk_free_rate=request.risk_free_rate,
        max_weight=request.max_weight
    )

    allocations = {}

    for symbol, weight in zip(
        prices.columns,
        result["weights"]
    ):
        allocations[str(symbol).upper()] = weight

    market_statistics = {}

    for symbol, expected_return in zip(
        prices.columns,
        expected_returns
    ):
        market_statistics[str(symbol).upper()] = {
            "expected_return": round(
                float(expected_return),
                4
            )
        }

    return {
        "objective": request.objective,
        "period": request.period,
        "allocations": allocations,
        "expected_return":
            result["expected_return"],
        "volatility":
            result["volatility"],
        "sharpe_ratio":
            result["sharpe_ratio"],
        "market_statistics":
            market_statistics
    }

@router.post("/optimize-for-profile")
def optimize_for_profile(
    request: ProfileOptimizerRequest
):

    if not (
        len(request.symbols)
        == len(request.asset_types)
        == len(request.sectors)
    ):
        raise ValueError(
            "symbols, asset_types and sectors "
            "must have the same length."
        )

    risk_profile = get_risk_profile(
        request.profile
    )

    prices = get_multiple_close_prices(
        request.symbols,
        request.period
    )

    expected_returns, covariance_matrix = (
        calculate_market_statistics(prices)
    )

    result = optimize_portfolio_with_constraints(
        expected_returns=
            expected_returns.tolist(),

        covariance_matrix=
            covariance_matrix.tolist(),

        asset_types=request.asset_types,
        sectors=request.sectors,

        max_single_asset=
            risk_profile["max_single_asset"],

        max_equity=
            risk_profile["max_equity"],

        min_bonds=
            risk_profile["min_bonds"],

        max_sector=
            risk_profile["max_sector"],

        objective=request.objective,

        risk_free_rate=
            request.risk_free_rate
    )

    allocations = {}

    for symbol, weight in zip(
        prices.columns,
        result["weights"]
    ):
        allocations[str(symbol).upper()] = weight

    return {
        "risk_profile": risk_profile,
        "objective": request.objective,
        "period": request.period,
        "allocations": allocations,
        "expected_return":
            result["expected_return"],
        "volatility":
            result["volatility"],
        "sharpe_ratio":
            result["sharpe_ratio"]
    }

@router.post("/backtest")
def backtest(request: BacktestRequest):

    if len(request.symbols) != len(
        request.weights
    ):
        raise ValueError(
            "Symbols and weights must have "
            "the same length."
        )

    symbols_to_download = list(
        dict.fromkeys(
            request.symbols
            + [request.benchmark]
        )
    )

    prices = get_multiple_close_prices(
        symbols_to_download,
        request.period
    )

    return run_backtest(
        prices=prices,
        symbols=[
            symbol.upper()
            for symbol in request.symbols
        ],
        weights=request.weights,
        benchmark=request.benchmark.upper(),
        risk_free_rate=request.risk_free_rate
    )


@router.get("/stress-test/presets")
def stress_test_presets():
    return get_available_scenarios()


@router.post("/stress-test")
def stress_test(request: StressTestRequest):
    return run_stress_test(
        request.portfolio,
        request.scenario.model_dump(),
    )


@router.post("/stress-test/preset/{preset}")
def stress_test_with_preset(preset: str, portfolio: Portfolio):
    return run_stress_test(portfolio, get_preset_scenario(preset))


@router.post("/chart-data")
def chart_data(request: ChartDataRequest):
    if request.scenario is None:
        return portfolio_chart_data(request.portfolio)
    return stress_chart_data(
        request.portfolio,
        request.scenario.model_dump(),
    )

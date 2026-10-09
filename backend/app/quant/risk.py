import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_returns(prices: list[float]) -> pd.Series:
    if len(prices) < 2:
        raise ValueError("At least two prices are required.")

    series = pd.Series(prices, dtype=float)

    return series.pct_change().dropna()


def annualized_return(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0

    compounded_growth = (1 + returns).prod()

    number_of_years = len(returns) / TRADING_DAYS

    if number_of_years <= 0:
        return 0.0

    return compounded_growth ** (1 / number_of_years) - 1


def annualized_volatility(returns: pd.Series) -> float:
    if returns.empty:
        return 0.0

    return float(
        returns.std() * np.sqrt(TRADING_DAYS)
    )


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.03
) -> float:

    annual_return = annualized_return(returns)
    volatility = annualized_volatility(returns)

    if volatility == 0:
        return 0.0

    return (
        annual_return - risk_free_rate
    ) / volatility


def max_drawdown(prices: list[float]) -> float:
    if not prices:
        return 0.0

    series = pd.Series(prices, dtype=float)

    running_max = series.cummax()

    drawdown = (
        series - running_max
    ) / running_max

    return float(drawdown.min())


def historical_var(
    returns: pd.Series,
    confidence: float = 0.95
) -> float:

    if returns.empty:
        return 0.0

    percentile = (1 - confidence) * 100

    return float(
        np.percentile(returns, percentile)
    )


def calculate_risk_metrics(
    prices: list[float],
    risk_free_rate: float = 0.03
) -> dict:

    returns = calculate_returns(prices)

    return {
        "annualized_return": round(
            annualized_return(returns), 4
        ),
        "annualized_volatility": round(
            annualized_volatility(returns), 4
        ),
        "sharpe_ratio": round(
            sharpe_ratio(
                returns,
                risk_free_rate
            ),
            4
        ),
        "max_drawdown": round(
            max_drawdown(prices),
            4
        ),
        "var_95_daily": round(
            historical_var(
                returns,
                confidence=0.95
            ),
            4
        )
    }
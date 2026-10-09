import numpy as np
import pandas as pd

from app.quant.risk import (
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown
)


def run_backtest(
    prices: pd.DataFrame,
    symbols: list[str],
    weights: list[float],
    benchmark: str,
    risk_free_rate: float = 0.03
) -> dict:

    if len(symbols) != len(weights):
        raise ValueError(
            "Symbols and weights must have the same length."
        )

    if not np.isclose(sum(weights), 1.0, atol=0.001):
        raise ValueError(
            "Portfolio weights must sum to 1.0."
        )

    missing_symbols = [
        symbol
        for symbol in symbols
        if symbol not in prices.columns
    ]

    if missing_symbols:
        raise ValueError(
            f"Missing market data for: {missing_symbols}"
        )

    if benchmark not in prices.columns:
        raise ValueError(
            f"Missing benchmark data for {benchmark}"
        )

    returns = prices.pct_change().dropna()

    portfolio_returns = returns[symbols].dot(
        np.array(weights)
    )

    benchmark_returns = returns[benchmark]

    # Start both at 1.0
    portfolio_growth = (
        1 + portfolio_returns
    ).cumprod()

    benchmark_growth = (
        1 + benchmark_returns
    ).cumprod()

    portfolio_total_return = (
        portfolio_growth.iloc[-1] - 1
    )

    benchmark_total_return = (
        benchmark_growth.iloc[-1] - 1
    )

    portfolio_metrics = {
        "total_return": round(
            float(portfolio_total_return),
            4
        ),
        "annualized_return": round(
            float(
                annualized_return(
                    portfolio_returns
                )
            ),
            4
        ),
        "annualized_volatility": round(
            float(
                annualized_volatility(
                    portfolio_returns
                )
            ),
            4
        ),
        "sharpe_ratio": round(
            float(
                sharpe_ratio(
                    portfolio_returns,
                    risk_free_rate
                )
            ),
            4
        ),
        "max_drawdown": round(
            float(
                max_drawdown(
                    portfolio_growth.tolist()
                )
            ),
            4
        )
    }

    benchmark_metrics = {
        "total_return": round(
            float(benchmark_total_return),
            4
        ),
        "annualized_return": round(
            float(
                annualized_return(
                    benchmark_returns
                )
            ),
            4
        ),
        "annualized_volatility": round(
            float(
                annualized_volatility(
                    benchmark_returns
                )
            ),
            4
        ),
        "sharpe_ratio": round(
            float(
                sharpe_ratio(
                    benchmark_returns,
                    risk_free_rate
                )
            ),
            4
        ),
        "max_drawdown": round(
            float(
                max_drawdown(
                    benchmark_growth.tolist()
                )
            ),
            4
        )
    }

    history = []

    for date in portfolio_growth.index:
        history.append({
            "date": date.strftime("%Y-%m-%d"),
            "portfolio": round(
                float(portfolio_growth.loc[date]),
                4
            ),
            "benchmark": round(
                float(benchmark_growth.loc[date]),
                4
            )
        })

    return {
        "portfolio_metrics": portfolio_metrics,
        "benchmark_metrics": benchmark_metrics,
        "history": history
    }
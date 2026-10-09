import numpy as np
from scipy.optimize import minimize


def portfolio_return(
    weights: np.ndarray,
    expected_returns: np.ndarray
) -> float:
    return float(np.dot(weights, expected_returns))


def portfolio_volatility(
    weights: np.ndarray,
    covariance_matrix: np.ndarray
) -> float:
    return float(
        np.sqrt(
            weights.T
            @ covariance_matrix
            @ weights
        )
    )


def negative_sharpe_ratio(
    weights: np.ndarray,
    expected_returns: np.ndarray,
    covariance_matrix: np.ndarray,
    risk_free_rate: float = 0.03
) -> float:

    expected_return = portfolio_return(
        weights,
        expected_returns
    )

    volatility = portfolio_volatility(
        weights,
        covariance_matrix
    )

    if volatility == 0:
        return 0.0

    sharpe = (
        expected_return - risk_free_rate
    ) / volatility

    return -sharpe
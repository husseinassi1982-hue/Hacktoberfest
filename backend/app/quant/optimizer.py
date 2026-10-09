import numpy as np
from scipy.optimize import minimize
import pandas as pd


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



def optimize_portfolio(
    expected_returns: list[float],
    covariance_matrix: list[list[float]],
    objective: str = "maximize_sharpe",
    risk_free_rate: float = 0.03,
    max_weight: float = 1.0
) -> dict:

    expected_returns_array = np.array(
        expected_returns,
        dtype=float
    )

    covariance_array = np.array(
        covariance_matrix,
        dtype=float
    )

    number_of_assets = len(
        expected_returns_array
    )

    if number_of_assets == 0:
        raise ValueError(
            "At least one asset is required."
        )

    if covariance_array.shape != (
        number_of_assets,
        number_of_assets
    ):
        raise ValueError(
            "Covariance matrix dimensions are invalid."
        )

    if max_weight <= 0 or max_weight > 1:
        raise ValueError(
            "max_weight must be between 0 and 1."
        )

    if number_of_assets * max_weight < 1:
        raise ValueError(
            "max_weight is too restrictive "
            "for the number of assets."
        )

    initial_weights = np.array(
        [1 / number_of_assets]
        * number_of_assets
    )

    bounds = [
        (0, max_weight)
        for _ in range(number_of_assets)
    ]

    constraints = [
        {
            "type": "eq",
            "fun": lambda weights:
                np.sum(weights) - 1
        }
    ]

    if objective == "maximize_sharpe":

        result = minimize(
            negative_sharpe_ratio,
            initial_weights,
            args=(
                expected_returns_array,
                covariance_array,
                risk_free_rate
            ),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints
        )

    elif objective == "minimize_volatility":

        result = minimize(
            portfolio_volatility,
            initial_weights,
            args=(covariance_array,),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints
        )

    else:
        raise ValueError(
            "Unsupported optimization objective."
        )

    if not result.success:
        raise ValueError(
            f"Optimization failed: {result.message}"
        )

    weights = result.x

    expected_return = portfolio_return(
        weights,
        expected_returns_array
    )

    volatility = portfolio_volatility(
        weights,
        covariance_array
    )

    sharpe = (
        (expected_return - risk_free_rate)
        / volatility
        if volatility > 0
        else 0
    )

    return {
        "weights": [
            round(float(weight), 4)
            for weight in weights
        ],
        "expected_return": round(
            expected_return,
            4
        ),
        "volatility": round(
            volatility,
            4
        ),
        "sharpe_ratio": round(
            sharpe,
            4
        )
    }

def calculate_market_statistics(
    prices: pd.DataFrame
) -> tuple[np.ndarray, np.ndarray]:

    returns = prices.pct_change().dropna()

    if returns.empty:
        raise ValueError(
            "Not enough historical data to calculate returns."
        )

    expected_returns = (
        returns.mean() * 252
    ).to_numpy()

    covariance_matrix = (
        returns.cov() * 252
    ).to_numpy()

    return (
        expected_returns,
        covariance_matrix
    )

def optimize_portfolio_with_constraints(
    expected_returns: list[float],
    covariance_matrix: list[list[float]],
    asset_types: list[str],
    sectors: list[str],
    max_single_asset: float,
    max_equity: float,
    min_bonds: float,
    max_sector: float,
    objective: str = "maximize_sharpe",
    risk_free_rate: float = 0.03
) -> dict:

    expected_returns_array = np.array(
        expected_returns,
        dtype=float
    )

    covariance_array = np.array(
        covariance_matrix,
        dtype=float
    )

    number_of_assets = len(expected_returns_array)

    if len(asset_types) != number_of_assets:
        raise ValueError(
            "asset_types must match number of assets."
        )

    if len(sectors) != number_of_assets:
        raise ValueError(
            "sectors must match number of assets."
        )

    if number_of_assets * max_single_asset < 1:
        raise ValueError(
            "The max single asset constraint makes "
            "the portfolio impossible to construct."
        )

    initial_weights = np.array(
        [1 / number_of_assets]
        * number_of_assets
    )

    bounds = [
        (0, max_single_asset)
        for _ in range(number_of_assets)
    ]

    constraints = []

    # Total allocation = 100%
    constraints.append({
        "type": "eq",
        "fun": lambda weights:
            np.sum(weights) - 1
    })

    # -------------------------
    # Equity constraint
    # -------------------------

    equity_indexes = [
        i
        for i, asset_type in enumerate(asset_types)
        if asset_type.lower()
        in ["stock", "equity_etf"]
    ]

    if equity_indexes:

        constraints.append({
            "type": "ineq",
            "fun": lambda weights:
                max_equity
                - np.sum(
                    weights[equity_indexes]
                )
        })

    # -------------------------
    # Bond constraint
    # -------------------------

    bond_indexes = [
        i
        for i, asset_type in enumerate(asset_types)
        if asset_type.lower()
        in ["bond", "bond_etf"]
    ]

    if min_bonds > 0 and not bond_indexes:
        raise ValueError(
            "Risk profile requires bonds, "
            "but no bond assets were provided."
        )

    if bond_indexes:

        constraints.append({
            "type": "ineq",
            "fun": lambda weights:
                np.sum(
                    weights[bond_indexes]
                )
                - min_bonds
        })

    # -------------------------
    # Sector constraints
    # -------------------------

    unique_sectors = set(sectors)

    for sector in unique_sectors:

        indexes = [
            i
            for i, current_sector
            in enumerate(sectors)
            if current_sector == sector
        ]

        constraints.append({
            "type": "ineq",
            "fun": lambda weights,
            indexes=indexes:
                max_sector
                - np.sum(weights[indexes])
        })

    # -------------------------
    # Objective
    # -------------------------

    if objective == "maximize_sharpe":

        result = minimize(
            negative_sharpe_ratio,
            initial_weights,
            args=(
                expected_returns_array,
                covariance_array,
                risk_free_rate
            ),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints
        )

    elif objective == "minimize_volatility":

        result = minimize(
            portfolio_volatility,
            initial_weights,
            args=(covariance_array,),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints
        )

    else:
        raise ValueError(
            "Unsupported optimization objective."
        )

    if not result.success:
        raise ValueError(
            f"Optimization failed: {result.message}"
        )

    weights = result.x

    expected_return = portfolio_return(
        weights,
        expected_returns_array
    )

    volatility = portfolio_volatility(
        weights,
        covariance_array
    )

    sharpe = (
        (expected_return - risk_free_rate)
        / volatility
        if volatility > 0
        else 0
    )

    return {
        "weights": [
            round(float(weight), 4)
            for weight in weights
        ],
        "expected_return": round(
            expected_return,
            4
        ),
        "volatility": round(
            volatility,
            4
        ),
        "sharpe_ratio": round(
            sharpe,
            4
        )
    }
import numpy as np


def run_monte_carlo(
    starting_value: float,
    monthly_contribution: float,
    years: int,
    expected_annual_return: float,
    annual_volatility: float,
    simulations: int = 10000,
    target_value: float | None = None,
    seed: int | None = 42
) -> dict:

    if starting_value <= 0:
        raise ValueError(
            "Starting value must be greater than zero."
        )

    if years <= 0:
        raise ValueError(
            "Years must be greater than zero."
        )

    months = years * 12

    dt = 1 / 12

    rng = np.random.default_rng(seed)

    paths = np.zeros(
        (simulations, months + 1)
    )

    paths[:, 0] = starting_value

    drift = (
        expected_annual_return
        - 0.5 * annual_volatility ** 2
    ) * dt

    monthly_volatility = (
        annual_volatility * np.sqrt(dt)
    )

    for month in range(1, months + 1):

        random_shocks = rng.normal(
            0,
            1,
            simulations
        )

        growth = np.exp(
            drift
            + monthly_volatility * random_shocks
        )

        paths[:, month] = (
            paths[:, month - 1] * growth
            + monthly_contribution
        )

    final_values = paths[:, -1]

    percentile_10 = np.percentile(
        final_values,
        10
    )

    percentile_50 = np.percentile(
        final_values,
        50
    )

    percentile_90 = np.percentile(
        final_values,
        90
    )

    result = {
        "simulations": simulations,
        "years": years,
        "starting_value": round(
            starting_value,
            2
        ),
        "monthly_contribution": round(
            monthly_contribution,
            2
        ),
        "final_value": {
            "percentile_10": round(
                float(percentile_10),
                2
            ),
            "median": round(
                float(percentile_50),
                2
            ),
            "percentile_90": round(
                float(percentile_90),
                2
            ),
            "mean": round(
                float(np.mean(final_values)),
                2
            )
        }
    }

    if target_value is not None:

        probability = np.mean(
            final_values >= target_value
        )

        result["target"] = {
            "value": target_value,
            "probability_of_reaching": round(
                float(probability),
                4
            )
        }

    return result
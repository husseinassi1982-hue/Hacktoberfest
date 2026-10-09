from app.models.portfolio import Portfolio


def analyze_portfolio(portfolio: Portfolio) -> dict:
    positions = []
    sector_values = {}

    invested_value = 0

    for position in portfolio.positions:
        market_value = position.quantity * position.price

        invested_value += market_value

        sector_values[position.sector] = (
            sector_values.get(position.sector, 0)
            + market_value
        )

        positions.append({
            "symbol": position.symbol,
            "quantity": position.quantity,
            "price": position.price,
            "market_value": market_value,
            "sector": position.sector,
            "asset_type": position.asset_type
        })

    total_value = invested_value + portfolio.cash

    # IMPORTANT: ajoute le poids à chaque position
    for position in positions:
        position["weight"] = (
            position["market_value"] / total_value
            if total_value > 0
            else 0
        )

    sector_allocation = {}

    for sector, value in sector_values.items():
        sector_allocation[sector] = {
            "value": value,
            "weight": (
                value / total_value
                if total_value > 0
                else 0
            )
        }

    cash_weight = (
        portfolio.cash / total_value
        if total_value > 0
        else 0
    )

    return {
        "total_value": total_value,
        "invested_value": invested_value,
        "cash": portfolio.cash,
        "cash_weight": cash_weight,
        "positions": positions,
        "sector_allocation": sector_allocation
    }
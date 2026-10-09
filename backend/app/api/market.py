from fastapi import APIRouter, HTTPException
from app.quant.risk import calculate_risk_metrics

from app.data.market import (
    get_current_price,
    get_historical_prices
)


router = APIRouter(
    prefix="/market",
    tags=["Market Data"]
)


@router.get("/price/{symbol}")
def price(symbol: str):

    try:
        return get_current_price(symbol)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get("/history/{symbol}")
def history(
    symbol: str,
    period: str = "1y"
):

    try:
        return get_historical_prices(
            symbol,
            period
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@router.get("/risk/{symbol}")
def risk(
    symbol: str,
    period: str = "1y"
):

    try:
        data = get_historical_prices(
            symbol,
            period
        )

        prices = [
            item["close"]
            for item in data["history"]
        ]

        metrics = calculate_risk_metrics(
            prices
        )

        return {
            "symbol": symbol.upper(),
            "period": period,
            "metrics": metrics
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

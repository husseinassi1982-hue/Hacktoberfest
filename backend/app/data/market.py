import yfinance as yf


def get_current_price(symbol: str) -> dict:
    symbol = symbol.upper()

    ticker = yf.Ticker(symbol)

    data = ticker.history(period="5d")

    if data.empty:
        raise ValueError(f"No market data found for {symbol}")

    latest = data.iloc[-1]

    return {
        "symbol": symbol,
        "price": round(float(latest["Close"]), 2),
        "open": round(float(latest["Open"]), 2),
        "high": round(float(latest["High"]), 2),
        "low": round(float(latest["Low"]), 2),
        "volume": int(latest["Volume"])
    }

def get_historical_prices(
    symbol: str,
    period: str = "1y"
) -> dict:

    symbol = symbol.upper()

    ticker = yf.Ticker(symbol)

    data = ticker.history(period=period)

    if data.empty:
        raise ValueError(f"No historical data found for {symbol}")

    history = []

    for date, row in data.iterrows():
        history.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(float(row["Open"]), 2),
            "high": round(float(row["High"]), 2),
            "low": round(float(row["Low"]), 2),
            "close": round(float(row["Close"]), 2),
            "volume": int(row["Volume"])
        })

    return {
        "symbol": symbol,
        "period": period,
        "history": history
    }
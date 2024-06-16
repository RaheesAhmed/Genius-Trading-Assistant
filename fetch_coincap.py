import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import dotenv
import logging

dotenv.load_dotenv()

api_key = os.getenv("COIN_MARKET_CAP_API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Fetch data from CoinMarketCap
def fetch_data(symbol, count=50, interval="weekly"):
    base_url = (
        "https://sandbox-api.coinmarketcap.com/v3/cryptocurrency/quotes/historical"
    )
    params = {
        "symbol": symbol,
        "count": count,
        "interval": interval,
    }

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }

    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()

    if response.status_code != 200:
        logger.error(f"Error fetching data: {response.status_code} - {data}")
        raise Exception(f"Error fetching data: {response.status_code} - {data}")

    if "data" not in data or symbol not in data["data"]:
        logger.error(f"Unexpected response format: {data}")
        raise KeyError(f"Unexpected response format: {data}")

    quotes = data["data"][symbol]["quotes"]
    df = pd.DataFrame(
        [
            {
                "date": datetime.fromisoformat(
                    quote["timestamp"].replace("Z", "+00:00")
                ),
                "close": quote["quote"]["USD"]["price"],
            }
            for quote in quotes
        ]
    )

    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

    return df


# Calculate Fibonacci Retracement Levels
def fibonacci_levels(high, low):
    levels = {
        "0%": low,
        "23.6%": low + (high - low) * 0.236,
        "38.2%": low + (high - low) * 0.382,
        "50%": low + (high - low) * 0.5,
        "61.8%": low + (high - low) * 0.618,
        "100%": high,
    }
    return levels


# Calculate SMA
def calculate_sma(data, window=14):
    if len(data) < window:
        logger.warning("Not enough data to calculate SMA")
        return np.nan
    return data["close"].rolling(window=window).mean().iloc[-1]


# Calculate RSI
def calculate_rsi(data, window=14):
    if len(data) < window:
        logger.warning("Not enough data to calculate RSI")
        return np.nan
    delta = data["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]  # Return the last value only


# Calculate MACD
def calculate_macd(data):
    exp1 = data["close"].ewm(span=12, adjust=False).mean()
    exp2 = data["close"].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd.iloc[-1], signal.iloc[-1]

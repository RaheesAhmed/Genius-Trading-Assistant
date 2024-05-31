import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# Fetch data
def fetch_data(ticker):
    today = datetime.today()
    start_date = (today - timedelta(days=14)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    data = yf.download(ticker, start=start_date, end=end_date)
    data.dropna(inplace=True)
    return data


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
def calculate_sma(data):
    return data["Close"].rolling(window=14).mean().iloc[-1]


# Calculate RSI
def calculate_rsi(data):
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]  # Return the last value only


# Calculate MACD
def calculate_macd(data):
    exp1 = data["Close"].ewm(span=12, adjust=False).mean()
    exp2 = data["Close"].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd.iloc[-1], signal.iloc[-1]

from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

my_updated_assistant = client.beta.assistants.update(
    assistant_id,
    instructions="You are a seasoned Crypto data analyst. Use the provided functions to retrieve data, calculate indicators, and develop trading strategies.",
    model="gpt-4o",
    name="Trade Genius",
    tools=[
        {"type": "code"},
        {
            "type": "function",
            "function": {
                "name": "fetch_data",
                "description": "Fetch 14 days of high, low, closing, and current market price data for a specific cryptocurrency pair",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The cryptocurrency pair, e.g., BTC-USD",
                        }
                    },
                    "required": ["ticker"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "fibonacci_levels",
                "description": "Calculate Fibonacci retracement levels using 14-day high and low prices",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "high": {
                            "type": "number",
                            "description": "The highest price in the last 14 days",
                        },
                        "low": {
                            "type": "number",
                            "description": "The lowest price in the last 14 days",
                        },
                    },
                    "required": ["high", "low"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_sma",
                "description": "Compute the 14-day Simple Moving Average (SMA) with daily closing prices",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Array of daily closing prices for the last 14 days",
                        }
                    },
                    "required": ["data"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_rsi",
                "description": "Calculate the 14-day Relative Strength Index (RSI)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Array of daily closing prices for the last 14 days",
                        }
                    },
                    "required": ["data"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_macd",
                "description": "Calculate the Moving Average Convergence Divergence (MACD) using 14-day closing prices",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Array of daily closing prices for the last 14 days",
                        }
                    },
                    "required": ["data"],
                },
            },
        },
    ],
)

print(my_updated_assistant)
print("Assistant updated successfully!")

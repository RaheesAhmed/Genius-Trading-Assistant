from openai import OpenAI
import time
import os
import dotenv
import json
from fetch_coincap import (
    fetch_data,
    fibonacci_levels,
    calculate_sma,
    calculate_rsi,
    calculate_macd,
)

dotenv.load_dotenv()


# uncommit the following lines if you are using the code in a Replit environment
# client.api_key = os.environ["OPEN_API_KEY"]
# assistant_id = os.environ["OPENAI_ASSISTANT_ID"]


# commit the following lines if you are using the code in a Replit environment
api_key = os.getenv("OPEN_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

client = OpenAI(api_key=api_key)


def extract_ticker_from_query(query):
    # Simple extraction logic (assuming the ticker is always at the end and formatted correctly)
    words = query.split()
    ticker = words[-1] if len(words[-1]) > 0 else None
    return ticker


def chat_with_assistant(user_query):
    try:
        # Extract ticker symbol from user query
        ticker = extract_ticker_from_query(user_query)
        if not ticker:
            return "No valid ticker symbol found in the query."

        # Create a thread and add a user message
        print("Creating thread...")
        thread = client.beta.threads.create()
        print(f"Thread created with ID: {thread.id}")

        print("Adding user message to thread...")
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_query,
        )
        print(f"User message added with ID: {message.id}")

        # Create and poll the run
        print("Creating and polling the run...")
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )
        print(f"Run created with status: {run.status}")

        while run.status == "requires_action":
            tool_outputs = []
            print("Run requires action. Processing tool calls...")

            for tool in run.required_action.submit_tool_outputs.tool_calls:
                print(f"Processing tool call for function: {tool.function.name}")

                if tool.function.name == "fetch_data":
                    data = fetch_data(ticker)
                    if data.empty:
                        print("No data fetched.")
                        tool_outputs.append(
                            {"tool_call_id": tool.id, "output": json.dumps(data)}
                        )
                    else:
                        data_output = data.to_dict(orient="records")
                        print("Fetched data:", data_output)
                        tool_outputs.append(
                            {"tool_call_id": tool.id, "output": json.dumps(data_output)}
                        )

                elif tool.function.name == "fibonacci_levels":
                    high = data["close"].max()
                    low = data["close"].min()
                    fib_levels = fibonacci_levels(high, low)
                    print("Calculated Fibonacci levels:", fib_levels)
                    tool_outputs.append(
                        {"tool_call_id": tool.id, "output": json.dumps(fib_levels)}
                    )

                elif tool.function.name == "calculate_sma":
                    sma = calculate_sma(data)
                    print("Calculated SMA:", sma)
                    tool_outputs.append({"tool_call_id": tool.id, "output": str(sma)})

                elif tool.function.name == "calculate_rsi":
                    rsi = calculate_rsi(data)
                    print("Calculated RSI:", rsi)
                    tool_outputs.append({"tool_call_id": tool.id, "output": str(rsi)})

                elif tool.function.name == "calculate_macd":
                    macd, signal = calculate_macd(data)
                    print("Calculated MACD and Signal:", macd, signal)
                    tool_outputs.append(
                        {
                            "tool_call_id": tool.id,
                            "output": json.dumps({"macd": macd, "signal": signal}),
                        }
                    )

            # Submit the tool outputs
            if tool_outputs:
                print("Submitting tool outputs...")
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
            else:
                print("No tool outputs to submit.")

            # Retrieve the run status again
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Current run status: {run.status}")

        # Poll for the final status of the run until completion
        while run.status not in ["completed", "failed"]:
            print("Run not completed. Polling again...")
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Current run status: {run.status}")

        # Check the final status of the run
        if run.status == "completed":
            print("Run completed. Fetching messages...")
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                print(message.content)
                return message.content[0].text.value
        else:
            print(f"Run ended with status: {run.status}")
            return "An error occurred. Please try again later."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An internal error occurred. Please try again later."

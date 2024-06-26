# Trade Genius Chatbot

The Trade Genius Chatbot is an innovative web application designed to provide users with a seamless interface for interacting with a cryptocurrency trading assistant. Built using Flask, this application serves a static files for chatbot interface that allows users to fetch real-time cryptocurrency data, perform technical analysis, and receive trading advice.

![Screenshot](static/images/screenshot.PNG)

## Project Structure

```
trading_assistant/
├── static/
│ ├── css/
│ │ └── styles.css
│ ├── js/
│ │ └── script.js
│ └── index.html
├── main.py
├── chat_with_assistant.py
├── fetch_crypto_prices.py
├── .env
└── README.md
```

## Features

`Serve Static Files:` Serve HTML, CSS, and JavaScript files for the chatbot interface.

`Chat Endpoint:` Provide a REST API endpoint to interact with the chatbot.

`Cryptocurrency Data Analysis:` Fetch cryptocurrency data and calculate technical indicators like Fibonacci levels, SMA, RSI, and MACD.

## Setup & Installation

1. Clone the repository:

```
git clone https://github.com/RaheesAhmed/Genius-Trading-Assistant.git

```

go to the directory

```
cd Genius-Trading-Assistant
```

2. Install the required packages:

```
pip install flask yfinance pandas numpy openai python-dotenv flask-cors

```

or

```
pip install -r requirments.txt
```

3. Create a .env file in the root directory and add your OpenAI API credentials:

```
OPENAI_API_KEY=your_openai_api_key
OPENAI_ASSISTANT_ID=your_openai_assistant_id
```

## Usage

Running the Application
To run the Flask application:

```
python main.py
```

Navigate to `http://localhost:5000` in your web browser to access the chatbot interface.

**_API Endpoints_**
`GET /chat`
Returns a welcome message.

`POST /chat`
Interacts with the chatbot. Send a JSON payload with the user query:

```
{
  "query": "Your query here"
}
```

### Example Response

```
{
  "response": "Chatbot's response"
}
```

### Files

`main.py`
This is the main Flask application file.

`chat_with_assistant.py`
This file contains the chat_with_assistant function which interacts with the OpenAI API.

`fetch_crypto_prices.py`
This file contains functions to fetch cryptocurrency data and calculate technical indicators.

### Developed By:

\***\*Rahees Ahmed\*\***
`Contact: raheesahmed256@gmail.com`

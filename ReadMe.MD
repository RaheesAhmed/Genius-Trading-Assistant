# Trade Genius Chatbot

This project is a Flask-based web application and a REST API that serves a static chatbot interface and provides a cryptocurrency trading assistant through a REST API. The chatbot can fetch cryptocurrency data, calculate various technical indicators, and provide trading advice.

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
git clone https://github.com/yourusername/my_flask_app.git
cd my_flask_app

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

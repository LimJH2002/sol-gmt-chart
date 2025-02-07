import datetime
import os

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from dotenv import load_dotenv  # Import load_dotenv
from flask import Flask, render_template, request

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)


def get_sol_gmt_data(interval="1d", days_back=90):
    """Fetches historical data with specified interval and days back."""

    if interval == "1d":
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days_back)
    elif interval == "1h":
        end_date = datetime.datetime.now()  # Use datetime for hourly
        start_date = end_date - datetime.timedelta(hours=days_back * 24)
    else:
        return None  # Invalid Interval

    try:
        sol_data = yf.download(
            "SOL-USD", start=start_date, end=end_date, interval=interval
        )
        gmt_data = yf.download(
            "GMT18069-USD", start=start_date, end=end_date, interval=interval
        )

        if sol_data.empty or gmt_data.empty:
            return None

        sol_data, gmt_data = sol_data.align(gmt_data, join="inner", axis=0)

        sol_gmt_data = pd.DataFrame()
        sol_gmt_data["Open"] = sol_data["Open"] / gmt_data["Open"]
        sol_gmt_data["High"] = sol_data["High"] / gmt_data["High"]
        sol_gmt_data["Low"] = sol_data["Low"] / gmt_data["Low"]
        sol_gmt_data["Close"] = sol_data["Close"] / gmt_data["Close"]
        sol_gmt_data["Volume"] = sol_data["Volume"]
        sol_gmt_data.index.name = "Date"

        return sol_gmt_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def create_candlestick_chart(data, interval):
    """Creates a Plotly candlestick chart."""
    if data is None:
        return "<div>Error: Could not fetch data.</div>"

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="SOL/GMT",
            )
        ]
    )

    fig.update_layout(
        title=f"SOL/GMT Candlestick Chart ({interval})",  # Include interval in title
        xaxis_title="Date",
        yaxis_title="Price (SOL/GMT)",
        xaxis_rangeslider_visible=False,
    )
    chart_div = pio.to_html(fig, full_html=False)
    return chart_div


@app.route("/")
def index():
    """Default route, shows daily chart."""
    return render_template("index.html", interval="1d")


@app.route("/chart")
def chart():
    """Route to handle chart requests with interval parameter."""
    interval = request.args.get(
        "interval", "1d"
    )  # Get interval from query parameter, default to '1d'
    days_back_str = request.args.get(
        "days_back", "90"
    )  # Get from query parameter, default 90
    try:
        days_back = int(days_back_str)
    except ValueError:
        days_back = 90

    sol_gmt_data = get_sol_gmt_data(interval=interval, days_back=days_back)
    chart_html = create_candlestick_chart(sol_gmt_data, interval)
    return chart_html


if __name__ == "__main__":
    # Use environment variables for port and debug mode
    port = int(os.environ.get("PORT", 5000))  # Get port from .env, default to 5000
    if os.environ.get("FLASK_ENV") == "production":
        app.run(debug=False, host="0.0.0.0", port=port)  # For Render/Heroku
    else:
        app.run(debug=True, host="0.0.0.0", port=port)  # For local use.

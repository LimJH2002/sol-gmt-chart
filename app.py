import datetime
import os

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from flask import Flask, render_template

app = Flask(__name__)


def get_sol_gmt_data(days_back=90):  # Fetch data for the last 'days_back' days.
    """Fetches historical data, calculates SOL/GMT, returns Plotly figure."""

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_back)

    try:
        sol_data = yf.download("SOL-USD", start=start_date, end=end_date)
        gmt_data = yf.download("GMT-USD", start=start_date, end=end_date)

        if sol_data.empty or gmt_data.empty:
            return None  # Or handle the error appropriately

        sol_data, gmt_data = sol_data.align(gmt_data, join="inner", axis=0)

        sol_gmt_data = pd.DataFrame()
        sol_gmt_data["Open"] = sol_data["Open"] / gmt_data["Open"]
        sol_gmt_data["High"] = sol_data["High"] / gmt_data["High"]
        sol_gmt_data["Low"] = sol_data["Low"] / gmt_data["Low"]
        sol_gmt_data["Close"] = sol_data["Close"] / gmt_data["Close"]
        sol_gmt_data["Volume"] = sol_data["Volume"]
        sol_gmt_data.index.name = "Date"  # Ensure 'Date' is the index name

        return sol_gmt_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def create_candlestick_chart(data):
    """Creates a Plotly candlestick chart from the given data."""
    if data is None:  # Handle the case where data fetching failed.
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
        title="SOL/GMT Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (SOL/GMT)",
        xaxis_rangeslider_visible=False,  # Remove the rangeslider
    )

    # Convert the Plotly figure to an HTML div
    chart_div = pio.to_html(fig, full_html=False)
    return chart_div


@app.route("/")
def index():
    """Main route. Fetches data, creates chart, renders template."""
    sol_gmt_data = get_sol_gmt_data()
    chart_html = create_candlestick_chart(sol_gmt_data)
    return render_template("index.html", chart=chart_html)


if __name__ == "__main__":
    # For local testing, use:
    # app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

    # Use for Render or Heroku:
    if os.environ.get("FLASK_ENV") == "production":
        app.run(debug=False)
    else:
        app.run(debug=True)

# SOL/GMT Candlestick Chart

[![Deployment Status](https://img.shields.io/badge/Deployment-Render-brightgreen)](YOUR_RENDER_APP_URL) <!-- Replace with your Render URL -->
[![Deployment Status](https://img.shields.io/badge/Deployment-Heroku-purple)](YOUR_HEROKU_APP_URL) <!-- Replace with your Heroku URL (if using)-->

This web application displays a live, interactive candlestick chart of the SOL/GMT exchange rate. It's built using Python, Flask, Plotly, and yfinance, and is deployed on Render (or Heroku) for 24/7 availability.

## Features

- **Interactive Candlestick Chart:** Uses Plotly to create a dynamic chart that allows users to zoom, pan, and hover over data points for details.
- **Automated Data Fetching:** Fetches historical price data for SOL-USD and GMT-USD from Yahoo Finance using the `yfinance` library.
- **SOL/GMT Calculation:** Calculates the SOL/GMT exchange rate from the fetched data.
- **Web Application:** Built with Flask, a lightweight Python web framework, to serve the chart as a web page.
- **Cloud Deployment:** Deployed on Render (recommended) or Heroku for continuous availability.

## Live Demo

[View the live chart here!](YOUR_RENDER_APP_URL) <!-- Replace with your Render URL -->

## Project Structure

sol-gmt-candlestick-chart/
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── templates/
│ └── index.html # HTML template for displaying the chart
└── static/
└── style.css # (Optional) CSS for styling

## Setup and Deployment

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- Git
- A Render account (recommended) or a Heroku account. A GitHub account is also highly recommended for easier deployment.

### Local Development (Running the app on your computer)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/sol-gmt-candlestick-chart.git  # Replace with your repo URL
   cd sol-gmt-candlestick-chart
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   python app.py
   ```

   The app will be accessible at `http://127.0.0.1:5000` (or a similar local address) in your web browser.

### Deployment to Render (Recommended)

1. **Create a Render Account:** Sign up at [https://render.com/](https://render.com/).

2. **Push your code to GitHub.**

3. **Create a New Web Service on Render:**

   - Connect your GitHub repository.
   - **Name:** Choose a name (e.g., `sol-gmt-chart`).
   - **Environment:** `Python 3`.
   - **Branch:** Your main branch (e.g., `main`).
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
   - **Advanced:**
   - Add an environment variable: `FLASK_ENV` with a value of `production`.
   - Add a second environment variable: `PORT` with value of `8080`.

4. **Deploy:** Click "Create Web Service". Render will provide you with a URL.

### Deployment to Heroku (Alternative)

1. **Create a Heroku Account:** Sign up at [https://www.heroku.com/](https://www.heroku.com/).
2. **Install Heroku CLI:** [https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli).
   3 **Login to Heroku CLI:** `heroku login`
3. **Create a `Procfile`:** (If not already present) In your project's root, create `Procfile` with: `web: gunicorn app:app`
4. **Initialize git**: `git init`, `git add .`, `git commit -m "Initial"`
5. **Create a Heroku App:** `heroku create your-app-name`
6. **Set Environment Variable:** `heroku config:set FLASK_ENV=production`
7. **Deploy:** `git push heroku main`
8. **Open the App:** `heroku open`

## Contributing

Feel free to open issues or submit pull requests for bug fixes, enhancements, or new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (You'll need to create a LICENSE file and put the MIT License text in it.)

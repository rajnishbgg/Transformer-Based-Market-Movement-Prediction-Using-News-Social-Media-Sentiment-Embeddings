# from flask import Flask, render_template, request
# from src.sentiment_model import SentimentAnalyzer

# app = Flask(__name__)
# analyzer = SentimentAnalyzer()

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/predict", methods=["POST"])
# def predict():
#     news_text = request.form["news"]

#     sentiment = analyzer.get_sentiment_score(news_text)

#     if sentiment == 1:
#         result = "Market Likely UP 📈"
#     elif sentiment == -1:
#         result = "Market Likely DOWN 📉"
#     else:
#         result = "Market Neutral ➖"

#     return render_template("index.html", prediction=result)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request
from src.sentiment_model import SentimentAnalyzer
import yfinance as yf
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
analyzer = SentimentAnalyzer()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    news = request.form["news"]
    ticker = request.form["ticker"]

    # Sentiment Analysis
    result = analyzer.analyze(news)

    # Download stock data (Last 1 Month)
    stock = yf.download(ticker, period="1mo")

    # Create graph
    if not os.path.exists("static"):
        os.makedirs("static")

    plt.figure(figsize=(8,4))
    stock["Close"].plot()
    plt.title(f"{ticker} - Last 30 Days Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)

    graph_path = "static/stock.png"
    plt.savefig(graph_path)
    plt.close()

    return render_template(
        "index.html",
        sentiment=result["sentiment"],
        confidence=result["confidence"],
        market=result["market"],
        graph=graph_path
    )

if __name__ == "__main__":
    app.run(debug=False)
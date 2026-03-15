import pandas as pd

from src.sentiment_model import SentimentAnalyzer
from src.stock_data import get_stock_data
from src.feature_engineering import merge_data
from src.train_model import train_model


def main():

    print("Step 1: Loading News Data...")
    news_df = pd.read_csv("data/news.csv")

    print("Step 2: Running LLM Sentiment Analysis...")
    analyzer = SentimentAnalyzer()
    news_df["Sentiment"] = news_df["News"].apply(
        analyzer.get_sentiment_score
    )

    print("Step 3: Downloading Stock Data...")
    stock_df = get_stock_data("AAPL")

    print("Step 4: Merging Data...")
    final_data = merge_data(stock_df, news_df)

    print("Step 5: Training Model...")
    train_model(final_data)

    print("Project Completed Successfully!")


if __name__ == "__main__":
    main()
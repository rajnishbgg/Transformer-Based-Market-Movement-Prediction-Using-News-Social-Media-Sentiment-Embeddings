import pandas as pd
import numpy as np

def merge_data(stock_df, news_df):

    # Convert date columns
    stock_df["Date"] = pd.to_datetime(stock_df["Date"])
    news_df["Date"] = pd.to_datetime(news_df["Date"])

    # Daily average sentiment
    news_daily = news_df.groupby("Date")["Sentiment"].mean().reset_index()

    # Merge
    merged = pd.merge(stock_df, news_daily, on="Date", how="left")

    merged["Sentiment"] = merged["Sentiment"].fillna(0)

    # Create Target (Next day movement)
    merged["Target"] = np.where(
        merged["Close"].shift(-1) > merged["Close"], 1, 0
    )

    return merged.dropna()
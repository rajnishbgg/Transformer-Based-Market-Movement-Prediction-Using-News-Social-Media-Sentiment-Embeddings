import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from src.sentiment_model import SentimentAnalyzer
from src.feature_engineering import merge_data
from src.train_model import train_model
import requests
import json

"""
LIVE DATA API INTEGRATION MODULE
Fetch real-time financial news and stock data through multiple APIs
"""

class NewsAPIConnector:
    """
    Fetch real-time news from NewsAPI
    API: https://newsapi.org/
    """
    
    def __init__(self, api_key):
        """
        Initialize with your NewsAPI key
        Get free key from: https://newsapi.org/
        """
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
    
    def get_financial_news(self, keywords, days=7):
        """
        Fetch financial news based on keywords
        
        Args:
            keywords (str): Search terms (e.g., "Apple earnings", "market crash")
            days (int): How many days back to search
        
        Returns:
            DataFrame with columns: title, description, source, publishedAt, url
        """
        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            to_date = datetime.now().strftime('%Y-%m-%d')
            
            url = f"{self.base_url}/everything"
            params = {
                'q': keywords,
                'from': from_date,
                'to': to_date,
                'sortBy': 'relevancy',
                'language': 'en',
                'apiKey': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'ok':
                print(f"Error: {data.get('message', 'Unknown error')}")
                return None
            
            articles = data['articles']
            df = pd.DataFrame([
                {
                    'title': article['title'],
                    'description': article['description'],
                    'source': article['source']['name'],
                    'publishedAt': article['publishedAt'],
                    'url': article['url']
                }
                for article in articles
            ])
            
            print(f"✓ Retrieved {len(df)} news articles")
            return df
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            return None


class FinancialDataAPI:
    """
    Fetch real-time financial data from multiple sources
    """
    
    @staticmethod
    def get_live_stock_data(ticker, period='1mo'):
        """
        Get live stock data from Yahoo Finance
        
        Args:
            ticker (str): Stock ticker (AAPL, TSLA, RELIANCE.NS, etc.)
            period (str): Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, etc.)
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            print(f"Fetching live data for {ticker}...")
            data = yf.download(ticker, period=period, progress=False)
            data.reset_index(inplace=True)
            print(f"✓ Retrieved {len(data)} trading days")
            return data
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return None
    
    @staticmethod
    def get_stock_info(ticker):
        """
        Get company information
        
        Args:
            ticker (str): Stock ticker
        
        Returns:
            Dictionary with company info
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            company_info = {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'current_price': info.get('currentPrice', 'N/A'),
                'description': info.get('longBusinessSummary', 'N/A')
            }
            
            return company_info
        except Exception as e:
            print(f"Error fetching company info: {e}")
            return None
    
    @staticmethod
    def get_multiple_stocks(tickers, period='1mo'):
        """
        Get data for multiple stocks
        
        Args:
            tickers (list): List of tickers
            period (str): Time period
        
        Returns:
            Dictionary with ticker: data pairs
        """
        results = {}
        for ticker in tickers:
            data = FinancialDataAPI.get_live_stock_data(ticker, period)
            if data is not None:
                results[ticker] = data
        
        return results


class LivePredictionPipeline:
    """
    Complete pipeline for live predictions with real data
    """
    
    def __init__(self, newsapi_key=None):
        """
        Initialize pipeline
        
        Args:
            newsapi_key (str): Your NewsAPI key (optional)
        """
        self.news_connector = NewsAPIConnector(newsapi_key) if newsapi_key else None
        self.sentiment_analyzer = SentimentAnalyzer()
        self.data_api = FinancialDataAPI()
    
    def predict_from_live_data(self, ticker, news_keywords, days=7):
        """
        Complete prediction pipeline using live data
        
        Args:
            ticker (str): Stock ticker
            news_keywords (str): Keywords for news search
            days (int): Days of historical data to use
        
        Returns:
            Dictionary with analysis results
        """
        
        print("=" * 70)
        print(f"LIVE PREDICTION PIPELINE FOR {ticker}")
        print("=" * 70)
        
        # Step 1: Fetch Live News
        print("\n[STEP 1] Fetching Live Financial News...")
        print("-" * 70)
        
        if self.news_connector:
            news_df = self.news_connector.get_financial_news(news_keywords, days)
            if news_df is None or len(news_df) == 0:
                print("⚠️  No news found. Using sample data.")
                news_df = pd.DataFrame({
                    'title': ['Sample news 1', 'Sample news 2'],
                    'publishedAt': [datetime.now(), datetime.now()]
                })
        else:
            print("⚠️  NewsAPI key not provided. Skipping live news.")
            news_df = None
        
        # Step 2: Analyze Sentiment
        print("\n[STEP 2] Analyzing Sentiment...")
        print("-" * 70)
        
        sentiments = []
        if news_df is not None:
            for idx, row in news_df.iterrows():
                title = str(row.get('title', ''))
                if title:
                    sentiment = self.sentiment_analyzer.analyze(title)
                    sentiments.append(sentiment)
                    print(f"[{idx+1}/{len(news_df)}] {title[:60]}...")
                    print(f"         → {sentiment['sentiment']} ({sentiment['confidence']}%)")
        
        # Step 3: Fetch Live Stock Data
        print("\n[STEP 3] Fetching Live Stock Data...")
        print("-" * 70)
        
        stock_data = self.data_api.get_live_stock_data(ticker, period=f'{days}d')
        
        if stock_data is None:
            print("❌ Failed to fetch stock data")
            return None
        
        # Step 4: Get Company Info
        print("\n[STEP 4] Retrieving Company Information...")
        print("-" * 70)
        
        company_info = self.data_api.get_stock_info(ticker)
        if company_info:
            print(f"Company: {company_info['name']}")
            print(f"Sector: {company_info['sector']}")
            print(f"Current Price: ${company_info['current_price']}")
            print(f"P/E Ratio: {company_info['pe_ratio']}")
        
        # Step 5: Prepare Data
        print("\n[STEP 5] Preparing Data for Prediction...")
        print("-" * 70)
        
        # Calculate average sentiment if available
        if sentiments:
            avg_sentiment = np.mean([s['confidence']/100 for s in sentiments])
        else:
            avg_sentiment = 0.5  # Neutral
        
        print(f"Average Sentiment Score: {avg_sentiment:.2f}")
        print(f"Recent Price: ${stock_data['Close'].iloc[-1]:.2f}")
        print(f"Volume: {stock_data['Volume'].iloc[-1]:,.0f}")
        
        # Step 6: Make Prediction
        print("\n[STEP 6] Making Prediction...")
        print("-" * 70)
        
        recent_volume = stock_data['Volume'].iloc[-1]
        avg_volume = stock_data['Volume'].mean()
        
        # Simple prediction logic
        prediction = self._predict(avg_sentiment, recent_volume)
        
        # Step 7: Results
        print("\n[RESULTS]")
        print("=" * 70)
        
        results = {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'sentiment': {
                'average': avg_sentiment,
                'label': 'Positive' if avg_sentiment > 0.6 else 'Negative' if avg_sentiment < 0.4 else 'Neutral',
                'count': len(sentiments)
            },
            'stock_data': {
                'current_price': float(stock_data['Close'].iloc[-1]),
                'volume': float(recent_volume),
                'avg_volume': float(avg_volume),
                '7_day_high': float(stock_data['High'].tail(7).max()),
                '7_day_low': float(stock_data['Low'].tail(7).min())
            },
            'prediction': prediction,
            'company_info': company_info
        }
        
        # Display results
        print(f"Ticker: {results['ticker']}")
        print(f"Sentiment: {results['sentiment']['label']} ({results['sentiment']['average']:.2%})")
        print(f"Current Price: ${results['stock_data']['current_price']:.2f}")
        print(f"Prediction: {results['prediction']['direction']} ({results['prediction']['confidence']:.1%} confidence)")
        print(f"Recommendation: {results['prediction']['recommendation']}")
        print("=" * 70)
        
        return results
    
    def _predict(self, sentiment, volume):
        """
        Simple prediction based on sentiment and volume
        """
        avg_volume_threshold = 40000000  # Average volume threshold
        
        if sentiment > 0.65 and volume > avg_volume_threshold:
            return {
                'direction': 'UP 📈',
                'confidence': min(0.95, 0.6 + sentiment * 0.35),
                'recommendation': 'STRONG BUY'
            }
        elif sentiment > 0.55:
            return {
                'direction': 'UP 📈',
                'confidence': min(0.85, 0.5 + sentiment * 0.35),
                'recommendation': 'BUY'
            }
        elif sentiment < 0.35 and volume > avg_volume_threshold:
            return {
                'direction': 'DOWN 📉',
                'confidence': min(0.95, (1 - sentiment) * 0.95),
                'recommendation': 'STRONG SELL'
            }
        elif sentiment < 0.45:
            return {
                'direction': 'DOWN 📉',
                'confidence': min(0.85, (1 - sentiment) * 0.85),
                'recommendation': 'SELL'
            }
        else:
            return {
                'direction': 'NEUTRAL ➖',
                'confidence': 0.5,
                'recommendation': 'HOLD'
            }
    
    def compare_multiple_stocks(self, tickers, days=7):
        """
        Compare predictions for multiple stocks
        
        Args:
            tickers (list): List of stock tickers
            days (int): Days of data
        
        Returns:
            DataFrame with comparison results
        """
        results = []
        
        for ticker in tickers:
            data = self.data_api.get_live_stock_data(ticker, period=f'{days}d')
            
            if data is not None:
                current_price = data['Close'].iloc[-1]
                volume = data['Volume'].iloc[-1]
                
                results.append({
                    'Ticker': ticker,
                    'Price': f'${current_price:.2f}',
                    'Volume': f'{volume/1e6:.1f}M',
                    '7D High': f'${data["High"].tail(7).max():.2f}',
                    '7D Low': f'${data["Low"].tail(7).min():.2f}',
                    'Change %': f'{((data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0] * 100):.2f}%'
                })
        
        comparison_df = pd.DataFrame(results)
        print("\n" + "=" * 100)
        print("STOCK COMPARISON")
        print("=" * 100)
        print(comparison_df.to_string(index=False))
        print("=" * 100)
        
        return comparison_df


# Usage Examples
if __name__ == "__main__":
    
    print("\n" + "=" * 70)
    print("LIVE DATA PREDICTION EXAMPLES")
    print("=" * 70)
    
    # Initialize pipeline without NewsAPI (for demo)
    pipeline = LivePredictionPipeline(newsapi_key=None)
    
    # Example 1: Single stock prediction
    print("\n\n### EXAMPLE 1: Single Stock Prediction ###\n")
    result = pipeline.predict_from_live_data(
        ticker='AAPL',
        news_keywords='Apple earnings technology',
        days=7
    )
    
    if result:
        print("\nJSON Output:")
        print(json.dumps(result, indent=2, default=str))
    
    # Example 2: Multiple stock comparison
    print("\n\n### EXAMPLE 2: Multiple Stock Comparison ###\n")
    tickers = ['AAPL', 'MSFT', 'TSLA', 'GOOGL']
    comparison = pipeline.compare_multiple_stocks(tickers, days=7)
    
    # Example 3: Real-time data fetching
    print("\n\n### EXAMPLE 3: Real-Time Data with Different Periods ###\n")
    for period in ['1d', '7d', '1mo']:
        print(f"\nFetching data for period: {period}")
        data = pipeline.data_api.get_live_stock_data('AAPL', period=period)
        if data is not None:
            print(f"Data shape: {data.shape}")
            print(f"Latest close: ${data['Close'].iloc[-1]:.2f}")


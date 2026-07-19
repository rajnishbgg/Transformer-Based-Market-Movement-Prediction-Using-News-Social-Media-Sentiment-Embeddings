# Live Data API Integration Guide

## 🌐 Real-Time Data Sources

This project now supports fetching **live financial news and stock data** through multiple APIs.

---

## 📚 Available APIs

### 1. **NewsAPI** - Financial News
```
Website: https://newsapi.org/
Type: REST API
Cost: Free tier available
Rate Limit: 500 requests/day (free)
```

**Features:**
- Get news from 40,000+ news sources
- Filter by keywords, language, date
- Real-time news articles
- Sentiment analysis ready

**Sign Up:**
1. Go to https://newsapi.org/
2. Click "Get API Key"
3. Enter email and create account
4. Copy your API key

### 2. **Yahoo Finance** - Stock Data (Already Integrated)
```
Website: https://finance.yahoo.com/
Library: yfinance (Python)
Cost: Free
Rate Limit: Reasonable limits
```

**Features:**
- Real-time stock prices
- Historical data
- Multiple time periods (1d, 7d, 1mo, 1y, etc.)
- Works for US and international stocks

---

## 🚀 Quick Start with Live Data

### **Step 1: Install Additional Dependencies**

```bash
pip install requests
```

### **Step 2: Get Your NewsAPI Key**

1. Visit https://newsapi.org/
2. Sign up for free account
3. Copy your API key from dashboard

### **Step 3: Run Live Prediction**

```python
from src.live_data_api import LivePredictionPipeline

# Initialize with your NewsAPI key
pipeline = LivePredictionPipeline(newsapi_key="YOUR_API_KEY_HERE")

# Get live prediction for Apple
result = pipeline.predict_from_live_data(
    ticker='AAPL',
    news_keywords='Apple earnings technology',
    days=7
)

print(result)
```

---

## 📋 API Usage Examples

### **Example 1: Fetch Live News**

```python
from src.live_data_api import NewsAPIConnector

connector = NewsAPIConnector(api_key="your_key_here")

# Get news about Apple from last 7 days
news_df = connector.get_financial_news(
    keywords="Apple earnings stock",
    days=7
)

print(news_df)
```

**Output:**
```
                                              title         source publishedAt
0  Apple Reports Record Q4 Earnings           Reuters  2024-01-25T10:30:00Z
1  AAPL Stock Surges on Strong iPhone Sales    CNBC  2024-01-24T14:15:00Z
2  Apple Announces New Product Launch           CNN   2024-01-23T08:00:00Z
```

### **Example 2: Get Live Stock Data**

```python
from src.live_data_api import FinancialDataAPI

# Get last 30 days of AAPL
data = FinancialDataAPI.get_live_stock_data('AAPL', period='1mo')

print(data.head())
```

**Output:**
```
        Date    Open    High     Low   Close        Volume
0 2024-01-02  175.43  177.20  174.50  176.50  52,000,000
1 2024-01-03  176.80  178.50  176.20  177.80  48,500,000
2 2024-01-04  177.50  179.20  177.00  178.90  51,200,000
...
```

### **Example 3: Get Company Information**

```python
from src.live_data_api import FinancialDataAPI

# Get Apple company info
info = FinancialDataAPI.get_stock_info('AAPL')

print(f"Company: {info['name']}")
print(f"Sector: {info['sector']}")
print(f"Market Cap: {info['market_cap']:,}")
print(f"Current Price: ${info['current_price']:.2f}")
print(f"P/E Ratio: {info['pe_ratio']:.2f}")
```

**Output:**
```
Company: Apple Inc
Sector: Technology
Market Cap: 2,850,000,000,000
Current Price: $178.50
P/E Ratio: 28.45
```

### **Example 4: Compare Multiple Stocks**

```python
from src.live_data_api import FinancialDataAPI

tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
data = FinancialDataAPI.get_multiple_stocks(tickers, period='1mo')

for ticker, df in data.items():
    print(f"\n{ticker}:")
    print(f"  Current: ${df['Close'].iloc[-1]:.2f}")
    print(f"  7-Day High: ${df['High'].tail(7).max():.2f}")
    print(f"  7-Day Low: ${df['Low'].tail(7).min():.2f}")
```

---

## 🔄 Complete Live Prediction Pipeline

### **Code Example:**

```python
from src.live_data_api import LivePredictionPipeline
import json

# Initialize
pipeline = LivePredictionPipeline(newsapi_key="YOUR_API_KEY")

# Run complete analysis
result = pipeline.predict_from_live_data(
    ticker='AAPL',
    news_keywords='Apple technology earnings',
    days=7
)

# Save results
with open('prediction_result.json', 'w') as f:
    json.dump(result, f, indent=2, default=str)

# Access individual results
print(f"Sentiment: {result['sentiment']['label']}")
print(f"Prediction: {result['prediction']['direction']}")
print(f"Confidence: {result['prediction']['confidence']:.1%}")
print(f"Recommendation: {result['prediction']['recommendation']}")
```

### **Output:**

```
======================================================================
LIVE PREDICTION PIPELINE FOR AAPL
======================================================================

[STEP 1] Fetching Live Financial News...
----------------------------------------------------------------------
✓ Retrieved 15 news articles

[STEP 2] Analyzing Sentiment...
----------------------------------------------------------------------
[1/15] Apple Reports Record Q4 Earnings...
       → Positive (95.2%)
[2/15] AAPL Faces Competition Challenges...
       → Negative (82.3%)
...

[STEP 3] Fetching Live Stock Data...
----------------------------------------------------------------------
✓ Retrieved 7 trading days

[STEP 4] Retrieving Company Information...
----------------------------------------------------------------------
Company: Apple Inc
Sector: Technology
Current Price: $178.50
P/E Ratio: 28.45

[STEP 5] Preparing Data for Prediction...
----------------------------------------------------------------------
Average Sentiment Score: 0.88
Recent Price: $178.50
Volume: 52,000,000

[STEP 6] Making Prediction...
----------------------------------------------------------------------

[RESULTS]
======================================================================
Ticker: AAPL
Sentiment: Positive (88.0%)
Current Price: $178.50
Prediction: UP 📈 (92.5% confidence)
Recommendation: STRONG BUY
======================================================================
```

---

## 🔌 API Specifications

### **NewsAPI Request**

```python
GET https://newsapi.org/v2/everything

Parameters:
- q: search query (required)
- from: start date (YYYY-MM-DD)
- to: end date (YYYY-MM-DD)
- sortBy: relevancy, publishedAt, popularity
- language: en, es, fr, etc.
- apiKey: your API key

Response:
{
    "status": "ok",
    "totalResults": 150,
    "articles": [
        {
            "source": {"id": null, "name": "Reuters"},
            "author": "John Doe",
            "title": "Apple Reports Record Earnings",
            "description": "Apple Inc reported...",
            "url": "https://...",
            "urlToImage": "https://...",
            "publishedAt": "2024-01-25T10:30:00Z",
            "content": "Full article content..."
        }
    ]
}
```

### **Yahoo Finance Data**

```python
import yfinance as yf

# Available periods:
# 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

data = yf.download('AAPL', period='1d')

# Returns DataFrame with:
# Date, Open, High, Low, Close, Adj Close, Volume
```

---

## 📊 Real-Time Monitoring Script

```python
from src.live_data_api import LivePredictionPipeline
import time
from datetime import datetime

pipeline = LivePredictionPipeline(newsapi_key="YOUR_API_KEY")

# Monitor stocks every hour
stocks_to_monitor = ['AAPL', 'MSFT', 'TSLA']

while True:
    print(f"\n[{datetime.now()}] Starting monitoring cycle...")
    
    for ticker in stocks_to_monitor:
        try:
            result = pipeline.predict_from_live_data(
                ticker=ticker,
                news_keywords=f"{ticker} earnings stock market",
                days=7
            )
            
            # Log results
            with open(f'{ticker}_monitoring.log', 'a') as f:
                f.write(f"{datetime.now()},{result['prediction']['direction']},"
                        f"{result['prediction']['confidence']}\n")
            
        except Exception as e:
            print(f"Error monitoring {ticker}: {e}")
    
    print("Waiting 1 hour before next check...")
    time.sleep(3600)  # Check every hour
```

---

## ⚙️ Configuration

### **Environment Variables (Optional)**

Create `.env` file:
```
NEWS_API_KEY=your_api_key_here
YFINANCE_CACHE=true
```

Load in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('NEWS_API_KEY')
```

---

## 🚨 Rate Limits & Considerations

### **NewsAPI Free Tier:**
- 500 requests per day
- ~1 request per 3 minutes
- Sufficient for personal use

### **Yahoo Finance:**
- No official API rate limits
- Recommended: 1-2 second delay between requests
- Large requests may be throttled

### **Best Practices:**

```python
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Use with NewsAPI
response = requests_retry_session().get(url, params=params)
```

---

## 📈 Data Pipeline Architecture

```
┌─────────────────────────────────────────────────────────┐
│              NEWS DATA COLLECTION                       │
│         NewsAPI → Financial News Articles               │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│          SENTIMENT ANALYSIS (FinBERT)                   │
│    Each article → Sentiment Score (0-1)                │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│          AGGREGATE SENTIMENT                            │
│    Multiple articles → Average Sentiment                │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌──────────��──────────────────────────────────────────────┐
│         STOCK DATA COLLECTION                           │
│      Yahoo Finance → Price, Volume, etc.               │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│       FEATURE ENGINEERING & PREDICTION                  │
│    Sentiment + Volume → Market Direction                │
└──────────────────┬──────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────┐
│          FINAL RECOMMENDATION                           │
│    BUY / SELL / HOLD with confidence scores            │
└─────────────────────────────────────────────────────────┘
```

---

## 🔗 Integration with Web App

Update `app.py` to use live data:

```python
from flask import Flask, render_template, request
from src.live_data_api import LivePredictionPipeline
import os

app = Flask(__name__)
pipeline = LivePredictionPipeline(
    newsapi_key=os.getenv('NEWS_API_KEY')
)

@app.route("/predict_live", methods=["POST"])
def predict_live():
    ticker = request.form["ticker"]
    
    # Get live prediction
    result = pipeline.predict_from_live_data(
        ticker=ticker,
        news_keywords=f"{ticker} earnings stock",
        days=7
    )
    
    return render_template(
        "results.html",
        sentiment=result['sentiment']['label'],
        confidence=f"{result['prediction']['confidence']:.1%}",
        market=result['prediction']['direction'],
        recommendation=result['prediction']['recommendation'],
        price=f"${result['stock_data']['current_price']:.2f}"
    )
```

---

## 📞 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid API key" | Verify key from newsapi.org dashboard |
| "Rate limit exceeded" | Wait before next request or upgrade plan |
| "No data available" | Check ticker symbol validity |
| "Connection timeout" | Check internet connection, retry |
| "401 Unauthorized" | Ensure API key is correct |

---

**Now you can use real-time data for live predictions! 🚀**

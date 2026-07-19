# 🚀 Setup and Run Guide

## Prerequisites
- Python 3.7+
- pip (Python package manager)

## Step 1: Install Dependencies

```bash
cd LLM_Market_Project
pip install -r requirements.txt
```

This will install:
- **pandas** - Data manipulation
- **numpy** - Numerical computations
- **scikit-learn** - Machine learning models
- **torch** - Deep learning framework (for transformers)
- **transformers** - HuggingFace transformers library (FinBERT model)
- **yfinance** - Yahoo Finance data fetching
- **flask** - Web framework

## Step 2: Choose Your Mode

### Option A: Command-Line Mode (Main Pipeline)
```bash
python main.py
```

**What it does:**
1. Loads sample news data from `data/news.csv`
2. Analyzes sentiment using FinBERT
3. Downloads historical stock data (AAPL, Jan 2022)
4. Merges sentiment data with stock data
5. Trains a Random Forest classifier
6. Displays model accuracy and classification report

**Output:**
```
Step 1: Loading News Data...
Step 2: Running LLM Sentiment Analysis...
Loading FinBERT model...
Step 3: Downloading Stock Data...
Step 4: Merging Data...
Step 5: Training Model...
Accuracy: 0.XX
Classification Report:
...
Project Completed Successfully!
```

### Option B: Web Application Mode (Flask)
```bash
python app.py
```

**What it does:**
- Starts a local web server at `http://localhost:5000`
- Provides interactive UI for predictions
- Displays stock price charts and sentiment analysis

**How to use:**
1. Open browser and go to `http://localhost:5000`
2. Enter financial news text
3. Enter stock ticker (e.g., AAPL, TSLA, RELIANCE.NS)
4. Click "Analyze Market"
5. View sentiment, confidence, and 30-day stock chart

## Troubleshooting

### Issue: "Module not found: transformers"
**Solution:** Make sure you installed all requirements
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Download failed for FinBERT model"
**Solution:** The model downloads automatically on first run. Ensure you have:
- Stable internet connection
- Enough disk space (~500MB)

### Issue: "No data available for ticker"
**Solution:** Make sure the ticker symbol is valid:
- US stocks: AAPL, MSFT, TSLA, etc.
- Indian stocks: Use `.NS` suffix (e.g., RELIANCE.NS, TCS.NS)

### Issue: "Date mismatch error in feature_engineering"
**Solution:** The sample data is from 2022. Update `main.py` with matching dates:
```python
stock_df = get_stock_data("AAPL", start="2022-01-01", end="2022-01-31")
```

## Project Architecture

```
LLM_Market_Project/
├── main.py                 # Main pipeline script
├── app.py                  # Flask web application
├── requirements.txt        # Python dependencies
├── data/
│   └── news.csv           # Sample financial news data
├── src/
│   ├── sentiment_model.py         # FinBERT sentiment analyzer
│   ├── stock_data.py              # Yahoo Finance data fetcher
│   ├── feature_engineering.py     # Data merging and features
│   └── train_model.py             # Model training logic
├── templates/
│   └── index.html         # Web UI template
└── static/
    └── style.css          # Web UI styling
```

## Model Details

- **Sentiment Model:** FinBERT (Fine-tuned BERT for financial texts)
- **Prediction Model:** Random Forest Classifier (100 trees)
- **Features Used:** Sentiment Score, Trading Volume
- **Target:** Binary classification (Market UP=1, DOWN=0)

## Notes

- First run will download FinBERT model (~500MB)
- Sample data is from January 2022
- The web app can download real-time data for any ticker
- Stock data is pulled from Yahoo Finance

---

For more information, see the main README.md

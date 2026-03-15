# import yfinance as yf

# def get_stock_data(symbol="AAPL",
#                    start="2022-01-01",
#                    end="2022-12-31"):

#     stock = yf.download(symbol, start=start, end=end)
#     stock.reset_index(inplace=True)
#     return stock

import yfinance as yf

def get_stock_data(symbol="AAPL",
                   start="2022-01-01",
                   end="2022-12-31"):

    stock = yf.download(symbol, start=start, end=end)

    stock.reset_index(inplace=True)

    # Ensure no multi-level columns
    stock.columns = [col if not isinstance(col, tuple) else col[0] for col in stock.columns]

    return stock
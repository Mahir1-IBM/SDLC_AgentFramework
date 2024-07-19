# filename: msft_stock_performance_2024.py
import subprocess
import sys

# Function to install a package if not already installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install yfinance if not already installed
try:
    import yfinance as yf
except ImportError:
    install('yfinance')
    import yfinance as yf

import pandas as pd

# Define the ticker symbol
ticker_symbol = 'MSFT'

# Define the date range
start_date = '2024-01-01'
end_date = '2024-12-31'

# Retrieve the stock data
msft_data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Filter the data to find days where the closing price was higher than $400
high_price_days = msft_data[msft_data['Close'] > 400]

# Print the result
if not high_price_days.empty:
    print("Dates when Microsoft stock was higher than $400 in 2024:")
    high_price_days_dates = high_price_days.index.strftime('%Y-%m-%d').tolist()
    for date in high_price_days_dates:
        print(date)
else:
    print("Microsoft stock was not higher than $400 on any day in 2024.")
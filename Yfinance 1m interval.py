import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the symbols for BANKBARODA, IOC, and PFC on NSE
symbols = ['BANKBARODA.NS', 'IOC.NS', 'PFC.NS']
interval = '1m'  # 1-minute interval

# Define the start date for the past week and set the end date to now
start_date = datetime.now() - timedelta(days=7)

# Create a new Excel writer object
output_file = f"Intraday_Historical_1Week_Data_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
with pd.ExcelWriter(output_file) as writer:
    # Function to get 1-minute interval data for the past week
    def get_1min_historical_data(symbol):
        # Fetch data from the start date to now
        stock_data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), interval=interval)

        # Filter for NSE trading hours (9:15 AM to 3:30 PM)
        stock_data = stock_data.between_time('09:15', '15:30')

        # Remove timezone information to avoid Excel compatibility issues
        stock_data.index = stock_data.index.tz_localize(None)

        return stock_data

    # Fetch and save data for each symbol in a separate Excel sheet
    for symbol in symbols:
        stock_data = get_1min_historical_data(symbol)
        if not stock_data.empty:
            # Write data to a separate sheet for each stock
            stock_data.to_excel(writer, sheet_name=symbol.replace('.NS', ''))

print(f"Historical 1-week data saved to {output_file}")

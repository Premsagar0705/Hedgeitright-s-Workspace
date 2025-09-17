import yfinance as yf
import datetime
import pandas as pd

# Define the ticker symbol for USD/INR
ticker = 'INR=X'

# Define the date range: 10 years from today
start_date = datetime.date.today() - datetime.timedelta(days=10*365)

# Download the historical data, including up to the current date
data = yf.download(ticker, start=start_date)

# Save the data to an Excel file
excel_file = 'usd_inr_10yr_data.xlsx'
data.to_excel(excel_file)

print(f"Data successfully saved to {excel_file}")

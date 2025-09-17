import yfinance as yf
import datetime
import pandas as pd

# Define the ticker symbol for USD/INR
ticker = 'EURUSD=X'

# Define the date range: 10 years from today until yesterday
start_date = datetime.date.today() - datetime.timedelta(days=10*365)
end_date = datetime.date.today() - datetime.timedelta(days=1)

# Download the historical data, including up to yesterday
data = yf.download(ticker, start=start_date, end=end_date)

# Save the data to an Excel file
excel_file = 'EUR_USD_10yr_data.xlsx'
data.to_excel(excel_file)

print(f"Data successfully saved to {excel_file}")

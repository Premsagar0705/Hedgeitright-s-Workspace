
# Stock options (Similarly for index options, set index = True)
from nsepy import get_history
from datetime import date
import pandas as pd

# Fetch historical option data for Apollo Tyres
stock_opt = get_history(
    symbol="APOLLOTYRE",
    start=date(2024, 12, 2),   # Start date for data retrieval
    end=date(2025, 1, 1),     # End date for data retrieval
    option_type="CE",          # Option type (CE for Call, PE for Put)
    strike_price=520,          # Strike price
    expiry_date=date(2025, 1, 30)  # Expiry date
)

# Display the first few rows of the retrieved data
print(stock_opt.head())

# Save to CSV
filename = "ApolloTyres_Options_CE_520_Jan30_2025.csv"
stock_opt.to_csv(filename, index=True)
print(f"Data saved to {filename}")

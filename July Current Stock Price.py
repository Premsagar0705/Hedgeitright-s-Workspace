import yfinance as yf  # type: ignore
import pandas as pd
from datetime import datetime

# Manually map missing ticker names
manual_map = {
    "AARTIIND": "AARTIIND.NS", "ACC": "ACC.NS", "Balkrishna Industries": "BALKRISIND.NS",
    "Birla soft": "BSOFT.NS", "Chambal fertilizer": "CHAMBLFERT.NS", "HINDCOPPER": "HINDCOPPER.NS",
    "M&M Finance": "M&MFIN.NS", "MGL": "MGL.NS"
}

# Your full list of company names (normalized spacing and capitalization)
companies = [
    "AARTIIND", "ABFRL", "ACC", "ADANIENT", "ADANIGREEN", "ADANIPORTS", "Ambuja Cement",
    "APOLLOHOSP", "Ashok Leyland", "ASIANPAINT", "ATGL", "Axis bank", "BAJAJ-AUTO", "BAJAJFINSV",
    "Balkrishna Industries", "Bandhan bank", "Bank of Baroda", "BEL", "Bharat Forage", "BHARTIARTL",
    "Bhel", "BPCL", "Birla soft", "Cesc", "Chambal fertilizer", "CIPLA", "Container corporation",
    "Crompton greaves", "Dabur", "Delhivery", "DLF", "DRREDDY", "Eicher motors", "Exide industries",
    "Federal bank", "GAIL", "Granules India", "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE",
    "HEROMOTOCO", "HINDALCO", "HINDCOPPER", "HINDUNILVR", "Hindustan zinc", "Hudco", "ICICIBANK",
    "ICICI Prudential", "Idea", "IEX", "IGL", "INDHOTEL", "INDUSINDBK", "Indus tower", "INFY",
    "IOC", "IRCTC", "Irfc", "ITC", "JIOFIN", "JSWSTEEL", "Kalyan jeweller", "KOTAKBANK", "Laurus labs",
    "LIC housing finance", "LT", "LT Finance", "M&M", "M&M Finance", "MANAPPURAM", "Marico", "MARUTI",
    "MGL", "NATIONALUM", "NCC", "NESTLEIND", "NMDC", "NTPC", "Oberoi reality", "ONGC", "PETRONET",
    "PFC", "PNB", "POWERGRID", "Rail Vikas Nigam", "Rbl bank", "REC", "Reliance", "SAIL", "SBILIFE",
    "SBIN", "SHRIRAMFIN", "SUNPHARMA", "TATACONSUM", "Tata motors", "TATAPOWER", "TATASTEEL", "TCS", "TECHM",
    "TITAN", "TRENT", "ULTRACEMCO", "UPL", "VEDL", "Wipro", "Yesbank", "Zomato"
]

# Base stock mapping (your previous one)
base_stock_map = {
    "ABFRL": "ABFRL.NS", "ADANIENT": "ADANIENT.NS", "ADANIGREEN": "ADANIGREEN.NS", "ADANIPORTS": "ADANIPORTS.NS",
    "Ambuja Cement": "AMBUJACEM.NS", "APOLLOHOSP": "APOLLOHOSP.NS", "Ashok Leyland": "ASHOKLEY.NS",
    "ASIANPAINT": "ASIANPAINT.NS", "ATGL": "ATGL.NS", "Axis bank": "AXISBANK.NS", "BAJAJ-AUTO": "BAJAJ-AUTO.NS",
    "BAJAJFINSV": "BAJAJFINSV.NS", "Bandhan bank": "BANDHANBNK.NS", "Bank of Baroda": "BANKBARODA.NS",
    "BEL": "BEL.NS", "Bharat Forage": "BHARATFORG.NS", "BHARTIARTL": "BHARTIARTL.NS", "Bhel": "BHEL.NS",
    "BPCL": "BPCL.NS", "Cesc": "CESC.NS", "CIPLA": "CIPLA.NS", "Coal India": "COALINDIA.NS",
    "Container corporation": "CONCOR.NS", "Crompton greaves": "CROMPTON.NS", "Dabur": "DABUR.NS",
    "Delhivery": "DELHIVERY.NS", "DLF": "DLF.NS", "DRREDDY": "DRREDDY.NS", "Eicher motors": "EICHERMOT.NS",
    "Exide industries": "EXIDEIND.NS", "Federal bank": "FEDERALBNK.NS", "GAIL": "GAIL.NS",
    "Granules India": "GRANULES.NS", "GRASIM": "GRASIM.NS", "HCLTECH": "HCLTECH.NS", "HDFCBANK": "HDFCBANK.NS",
    "HDFCLIFE": "HDFCLIFE.NS", "HEROMOTOCO": "HEROMOTOCO.NS", "HINDALCO": "HINDALCO.NS",
    "HINDUNILVR": "HINDUNILVR.NS", "Hindustan zinc": "HINDZINC.NS", "Hudco": "HUDCO.NS",
    "ICICIBANK": "ICICIBANK.NS", "ICICI Prudential": "ICICIPRULI.NS", "Idea": "IDEA.NS", "IEX": "IEX.NS",
    "IGL": "IGL.NS", "INDHOTEL": "INDHOTEL.NS", "INDUSINDBK": "INDUSINDBK.NS", "Indus tower": "INDUSTOWER.NS",
    "INFY": "INFY.NS", "IOC": "IOC.NS", "IRCTC": "IRCTC.NS", "Irfc": "IRFC.NS", "ITC": "ITC.NS",
    "JIOFIN": "JIOFIN.NS", "JSWSTEEL": "JSWSTEEL.NS", "Kalyan jeweller": "KALYANKJIL.NS",
    "KOTAKBANK": "KOTAKBANK.NS", "Laurus labs": "LAURUSLABS.NS", "LIC housing finance": "LICHSGFIN.NS",
    "LT": "LT.NS", "LT Finance": "LTF.NS", "M&M": "M&M.NS", "MANAPPURAM": "MANAPPURAM.NS",
    "Marico": "MARICO.NS", "MARUTI": "MARUTI.NS", "NATIONALUM": "NATIONALUM.NS", "NCC": "NCC.NS",
    "NESTLEIND": "NESTLEIND.NS", "NMDC": "NMDC.NS", "NTPC": "NTPC.NS", "Oberoi reality": "OBEROIRLTY.NS",
    "ONGC": "ONGC.NS", "PETRONET": "PETRONET.NS", "PFC": "PFC.NS", "PNB": "PNB.NS", "POWERGRID": "POWERGRID.NS",
    "Rail Vikas Nigam": "RVNL.NS", "Rbl bank": "RBLBANK.NS", "REC": "RECLTD.NS", "Reliance": "RELIANCE.NS",
    "SAIL": "SAIL.NS", "SBILIFE": "SBILIFE.NS","SBIN": "SBIN.NS", "SHRIRAMFIN": "SHRIRAMFIN.NS", "SUNPHARMA": "SUNPHARMA.NS",
    "TATACONSUM": "TATACONSUM.NS", "Tata motors": "TATAMOTORS.NS", "TATAPOWER": "TATAPOWER.NS",
    "TATASTEEL": "TATASTEEL.NS", "TCS": "TCS.NS", "TECHM": "TECHM.NS", "TITAN": "TITAN.NS", "TRENT": "TRENT.NS",
    "ULTRACEMCO": "ULTRACEMCO.NS", "UPL": "UPL.NS", "VEDL": "VEDL.NS", "Wipro": "WIPRO.NS",
    "Yesbank": "YESBANK.NS", "Zomato": "ETERNAL.NS"
}

# Merge the maps
full_stock_map = {**base_stock_map, **manual_map}

# Create ticker list
tickers = [full_stock_map[comp] for comp in companies if comp in full_stock_map]

# Download all data in one batch
print("📥 Downloading data for all stocks...")
data = yf.download(tickers, period="1d", group_by="ticker", auto_adjust=False, progress=False)

# Extract close prices
results = []
for company in companies:
    ticker = full_stock_map.get(company)
    try:
        close = data[ticker]["Close"].iloc[-1] if ticker in data.columns.levels[0] else "No Data"
    except Exception:
        close = "Error"
    results.append([company, ticker or "N/A", close])

# Save to Excel
df = pd.DataFrame(results, columns=["Company", "Ticker", "Current Price"])
filename = f"batch_stock_prices_{datetime.today().strftime('%d-%m-%Y')}.xlsx"
df.to_excel(filename, index=False, engine="openpyxl")

print(f"✅ Done! File saved as {filename}")

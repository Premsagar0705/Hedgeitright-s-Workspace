import yfinance as yf  # type: ignore
import pandas as pd

# Mapping: Company Name => Ticker
stocks = {
    "AARTIIND": "AARTIIND.NS", "ABFRL": "ABFRL.NS", "ACC": "ACC.NS", "ADANIENT": "ADANIENT.NS",
    "ADANIGREEN": "ADANIGREEN.NS", "ADANIPORTS": "ADANIPORTS.NS", "Ambuja Cement": "AMBUJACEM.NS",
    "APOLLOHOSP": "APOLLOHOSP.NS", "Ashok Leyland": "ASHOKLEY.NS", "ASIANPAINT": "ASIANPAINT.NS",
    "ATGL": "ATGL.NS", "Axis bank": "AXISBANK.NS", "BAJAJ-AUTO": "BAJAJ-AUTO.NS",
    "BAJAJFINSV": "BAJAJFINSV.NS", "Balkrishna Industries": "BALKRISIND.NS",
    "Bandhan bank": "BANDHANBNK.NS", "Bank of Baroda": "BANKBARODA.NS", "BEL": "BEL.NS",
    "Bharat Forage": "BHARATFORG.NS", "BHARTIARTL": "BHARTIARTL.NS", "Bhel": "BHEL.NS",
    "BPCL": "BPCL.NS", "Birla soft": "BSOFT.NS", "Cesc": "CESC.NS", "Chambal fertilizer": "CHAMBLFERT.NS",
    "CIPLA": "CIPLA.NS", "Container corporation": "CONCOR.NS", "Crompton greaves": "CROMPTON.NS",
    "Dabur": "DABUR.NS", "Delhivery": "DELHIVERY.NS", "DLF": "DLF.NS", "DRREDDY": "DRREDDY.NS",
    "Eicher motors": "EICHERMOT.NS", "Exide industries": "EXIDEIND.NS", "Federal bank": "FEDERALBNK.NS",
    "GAIL": "GAIL.NS", "Granules India": "GRANULES.NS", "GRASIM": "GRASIM.NS", "HCLTECH": "HCLTECH.NS",
    "HDFCBANK": "HDFCBANK.NS", "HDFCLIFE": "HDFCLIFE.NS", "HEROMOTOCO": "HEROMOTOCO.NS",
    "HINDALCO": "HINDALCO.NS", "HINDCOPPER": "HINDCOPPER.NS", "HINDUNILVR": "HINDUNILVR.NS",
    "Hindustan zinc": "HINDZINC.NS", "Hudco": "HUDCO.NS", "ICICIBANK": "ICICIBANK.NS",
    "ICICI Prudential": "ICICIPRULI.NS", "Idea": "IDEA.NS", "IEX": "IEX.NS", "IGL": "IGL.NS",
    "INDHOTEL": "INDHOTEL.NS", "INDUSINDBK": "INDUSINDBK.NS", "Indus tower": "INDUSTOWER.NS",
    "INFY": "INFY.NS", "IOC": "IOC.NS", "IRCTC": "IRCTC.NS", "Irfc": "IRFC.NS", "ITC": "ITC.NS",
    "JIOFIN": "JIOFIN.NS", "JSWSTEEL": "JSWSTEEL.NS", "Kalyan jeweller": "KALYANKJIL.NS",
    "KOTAKBANK": "KOTAKBANK.NS", "Laurus labs": "LAURUSLABS.NS", "LIC housing finance": "LICHSGFIN.NS",
    "LT": "LT.NS", "LT Finance": "LTF.NS", "M&M": "M&M.NS", "M&M Finance": "M&MFIN.NS",
    "MANAPPURAM": "MANAPPURAM.NS", "Marico": "MARICO.NS", "MARUTI": "MARUTI.NS", "MGL": "MGL.NS",
    "NATIONALUM": "NATIONALUM.NS", "NCC": "NCC.NS", "NESTLEIND": "NESTLEIND.NS", "NMDC": "NMDC.NS",
    "NTPC": "NTPC.NS", "Oberoi reality": "OBEROIRLTY.NS", "ONGC": "ONGC.NS", "PETRONET": "PETRONET.NS",
    "PFC": "PFC.NS", "PNB": "PNB.NS", "POWERGRID": "POWERGRID.NS", "Rail Vikas Nigam": "RVNL.NS",
    "Rbl bank": "RBLBANK.NS", "REC": "RECLTD.NS", "Reliance": "RELIANCE.NS", "SAIL": "SAIL.NS",
    "SBILIFE": "SBILIFE.NS", "SHRIRAMFIN": "SHRIRAMFIN.NS", "SUNPHARMA": "SUNPHARMA.NS",
    "TATACONSUM": "TATACONSUM.NS", "Tata motors": "TATAMOTORS.NS", "TATAPOWER": "TATAPOWER.NS",
    "TATASTEEL": "TATASTEEL.NS", "TCS": "TCS.NS", "TECHM": "TECHM.NS", "TITAN": "TITAN.NS",
    "TRENT": "TRENT.NS", "ULTRACEMCO": "ULTRACEMCO.NS", "UPL": "UPL.NS", "VEDL": "VEDL.NS",
    "Wipro": "WIPRO.NS", "Yesbank": "YESBANK.NS", "ETERNAL": "ETERNAL.NS"
}

target_date = "2025-07-02"
end_date = "2025-07-03"

# Results will be stored here
stock_data_list = []

# Loop to fetch price
for company_name, ticker in stocks.items():
    try:
        print(f"✅ Fetching data for {company_name} ({ticker}) on {target_date}...")
        stock_info = yf.Ticker(ticker)
        hist = stock_info.history(start=target_date, end=end_date)

        if not hist.empty:
            close_price = hist["Close"].iloc[-1]
        else:
            close_price = "No Data"

        stock_data_list.append([company_name, ticker, close_price])
    except Exception as e:
        print(f"❌ Failed to fetch data for {company_name} ({ticker}): {e}")
        stock_data_list.append([company_name, ticker, "N/A"])

# Create DataFrame
df = pd.DataFrame(stock_data_list, columns=["Company", "Ticker", f"Close Price on {target_date}"])

# Save to Excel
file_name = f"stock_prices_{target_date.replace('-', '')}.xlsx"
df.to_excel(file_name, index=False, engine='openpyxl')

print(f"🔥 Stock prices saved to {file_name}!")

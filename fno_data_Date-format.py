import yfinance as yf
import pandas as pd

# Mapping company names to NSE symbols
stocks = {
    "AARTIIND": "AARTIIND.NS", "ABFRL": "ABFRL.NS", "ACC": "ACC.NS", "Adani Green": "ADANIGREEN.NS",
    "Adani Power": "ADANIPOWER.NS", "Adani Total Gas": "ATGL.NS", "Adani Wilmar": "AWL.NS",
    "ADANIENT": "ADANIENT.NS", "Ambuja Cement": "AMBUJACEM.NS", "Apollo Tyres": "APOLLOTYRE.NS",
    "Ashok Leyland": "ASHOKLEY.NS", "Axis Bank": "AXISBANK.NS", "Balkrishna Industries": "BALKRISIND.NS",
    "Balrampur Chini": "BALRAMCHIN.NS", "Bandhan Bank": "BANDHANBNK.NS", "Bank of Baroda": "BANKBARODA.NS",
    "BEL": "BEL.NS", "Berger Paints": "BERGEPAINT.NS", "Bharat Forge": "BHARATFORG.NS", "BHEL": "BHEL.NS",
    "Birlasoft": "BSOFT.NS", "BPCL": "BPCL.NS", "CANFINHOME": "CANFINHOME.NS", "Castrol India": "CASTROLIND.NS",
    "Central Bank": "CENTRALBK.NS", "Century Plyboard": "CENTURYPLY.NS", "CESC": "CESC.NS",
    "Chambal Fertilizer": "CHAMBLFERT.NS", "City Union Bank": "CUB.NS", "Coal India": "COALINDIA.NS",
    "Container Corporation": "CONCOR.NS", "Crompton Greaves": "CROMPTON.NS", "Dabur": "DABUR.NS",
    "Delhivery": "DELHIVERY.NS", "DLF": "DLF.NS", "Eicher Motors": "EICHERMOT.NS", "Emami": "EMAMILTD.NS",
    "Exide Industries": "EXIDEIND.NS", "FACT": "FACT.NS", "Federal Bank": "FEDERALBNK.NS",
    "Finolex Industries": "FINPIPE.NS", "GAIL": "GAIL.NS", "GNFC": "GNFC.NS", "Granules India": "GRANULES.NS",
    "Gujarat Gas": "GUJGASLTD.NS", "HINDALCO": "HINDALCO.NS", "HINDCOPPER": "HINDCOPPER.NS",
    "HINDPETRO": "HINDPETRO.NS", "Hindustan Zinc": "HINDZINC.NS", "HUDCO": "HUDCO.NS",
    "ICICI Prudential": "ICICIPRULI.NS", "IDBI": "IDBI.NS", "Vodafone Idea": "IDEA.NS", "IEX": "IEX.NS",
    "IGL": "IGL.NS", "INDHOTEL": "INDHOTEL.NS", "Indus Tower": "INDUSTOWER.NS", "IndusInd Bank": "INDUSINDBK.NS",
    "IOB": "IOB.NS", "IOC": "IOC.NS", "IRCTC": "IRCTC.NS", "IRFC": "IRFC.NS", "Kalyan Jewellers": "KALYANKJIL.NS",
    "Laurus Labs": "LAURUSLABS.NS", "LIC Housing Finance": "LICHSGFIN.NS", "LT Finance": "LTF.NS",
    "M&M Finance": "M&MFIN.NS", "MANAPPURAM": "MANAPPURAM.NS", "Marico": "MARICO.NS", "MGL": "MGL.NS",
    "NATIONALUM": "NATIONALUM.NS", "NCC": "NCC.NS", "NMDC": "NMDC.NS", "NTPC": "NTPC.NS",
    "Oberoi Realty": "OBEROIRLTY.NS", "Ola electric": "OLAELEC.NS", "ONGC": "ONGC.NS", "Petronet LNG": "PETRONET.NS",
    "PFC": "PFC.NS", "POWERGRID": "POWERGRID.NS", "Punjab National Bank": "PNB.NS",
    "Quess Corp": "QUESS.NS", "Rail Vikas Nigam": "RVNL.NS", "RBL Bank": "RBLBANK.NS",
    "REC": "RECLTD.NS", "Reliance": "Reliance.NS", "SAIL": "SAIL.NS", "SBIN": "SBIN.NS",
    "Sun TV": "SUNTV.NS", "Suzlon Energy": "SUZLON.NS", "Swiggy": "SWIGGY.NS", "Tata Motors": "TATAMOTORS.NS",
    "TATAPOWER": "TATAPOWER.NS", "TATASTEEL": "TATASTEEL.NS", "UPL": "UPL.NS", "VEDL": "VEDL.NS",
    "Wipro": "WIPRO.NS", "Yes Bank": "YESBANK.NS", "Zomato": "ZOMATO.NS"
}

# Target date
target_date = "2025-03-03"

# Filter out stocks that don't have an NSE symbol
valid_stocks = {name: symbol for name, symbol in stocks.items() if symbol is not None}

try:
    print("Downloading stock data for", target_date)
    stock_data = yf.download(list(valid_stocks.values()), start=target_date, end="2025-03-04", interval="1d", auto_adjust=True)

    if not stock_data.empty:
        # Extract only closing prices
        stock_data = stock_data["Close"].reset_index()
        stock_data = stock_data.melt(id_vars="Date", var_name="Symbol", value_name="Close Price")
        stock_data.dropna(inplace=True)  # Remove stocks with missing data

        # Map NSE symbols back to company names
        stock_data["Company"] = stock_data["Symbol"].map({v: k for k, v in valid_stocks.items()})
        stock_data = stock_data[["Date", "Company", "Close Price"]]

        # Sort the data according to the given company name order
        stock_data["Company"] = pd.Categorical(stock_data["Company"], categories=stocks.keys(), ordered=True)
        stock_data.sort_values(by=["Date", "Company"], inplace=True)

        # Save to Excel
        file_name = f"Stock_Data_{target_date}.xlsx"
        stock_data.to_excel(file_name, sheet_name="Stock Data", index=False)
        print(f"✅ Download complete! Data saved to {file_name}")
    else:
        print("⚠️ No data found for the specified stocks.")

except Exception as e:
    print(f"❌ Error fetching data: {e}")

import requests
import pandas as pd
import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

# ✅ Ordered list of symbols (don't change order)
symbols = [
    "360ONE", "ABB", "ABCAPITAL", "ADANIENSOL", "ADANIENT", "ADANIGREEN", "ADANIPORTS",
    "ALKEM", "AMBER", "AMBUJACEM", "ANGELONE", "APLAPOLLO", "APOLLOHOSP", "ASHOKLEY",
    "ASIANPAINT", "ASTRAL", "AUBANK", "AUROPHARMA", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV",
    "BAJFINANCE", "BANDHANBNK", "BANKBARODA", "BANKINDIA", "BDL", "BEL",
    "BHARATFORG", "BHARTIARTL", "BHEL", "BIOCON", "BLUESTARCO", "BOSCHLTD", "BPCL",
    "BRITANNIA", "BSE", "CAMS", "CANBK", "CDSL", "CGPOWER", "CHOLAFIN", "CIPLA", "COALINDIA",
    "COFORGE", "COLPAL", "CONCOR", "CROMPTON", "CUMMINSIND", "CYIENT", "DABUR", "DALBHARAT",
    "DELHIVERY", "DIVISLAB", "DIXON", "DLF", "DMART", "DRREDDY", "EICHERMOT", "EXIDEIND",
    "FEDERALBNK", "FORTIS", "GAIL", "GLENMARK", "GMRAIRPORT", "GODREJCP",
    "GODREJPROP", "GRASIM", "HAL", "HAVELLS", "HCLTECH", "HDFCAMC", "HDFCBANK", "HDFCLIFE",
    "HEROMOTOCO", "HFCL", "HINDALCO", "HINDUNILVR", "HINDZINC", "HUDCO", "ICICIBANK",
    "ICICIGI", "ICICIPRULI", "IDEA", "IDFCFIRSTB", "IEX", "IGL", "IIFL", "INDHOTEL",
    "INDIANB", "INDIGO", "INDUSINDBK", "INDUSTOWER", "INFY", "INOXWIND", "IOC", "IRCTC",
    "IREDA", "IRFC", "ITC", "JINDALSTEL", "JIOFIN", "JSWENERGY", "JSWSTEEL", "JUBLFOOD",
    "KALYANKJIL", "KAYNES", "KEI", "KFINTECH", "KOTAKBANK", "KPITTECH", "LAURUSLABS",
    "LICHSGFIN", "LICI", "LODHA", "LT", "LTF", "LTIM", "LUPIN", "M%26M", "MANAPPURAM",
    "MANKIND", "MARICO", "MARUTI", "MAXHEALTH", "MAZDOCK", "MCX", "MFSL",
    "MOTHERSON", "MPHASIS", "MUTHOOTFIN", "NATIONALUM", "NAUKRI", "NBCC", "NCC", "NESTLEIND",
    "NHPC", "NMDC", "NTPC", "NUVAMA", "NYKAA", "OBEROIRLTY", "OFSS",
    "OIL", "ONGC", "PAGEIND", "PATANJALI", "PAYTM", "PERSISTENT", "PETRONET", "PFC", "PGEL",
    "PHOENIXLTD", "PIDILITIND", "PIIND", "PNB", "PNBHOUSING", "POLICYBZR", "POLYCAB",
    "POWERGRID", "PPLPHARMA", "PRESTIGE", "RBLBANK", "RECLTD", "RELIANCE", "RVNL", "SAIL",
    "SAMMAANCAP", "SBICARD", "SBILIFE", "SHREECEM", "SHRIRAMFIN", "SIEMENS", "SOLARINDS",
    "SONACOMS", "SRF", "SUNPHARMA", "SUPREMEIND", "SUZLON", "SYNGENE", "TATACONSUM",
    "TATAELXSI", "TATAMOTORS", "TATAPOWER", "TATASTEEL", "TATATECH", "TCS", "TECHM",
    "TITAGARH", "TITAN", "TORNTPHARM", "TORNTPOWER", "TRENT", "TVSMOTOR", "ULTRACEMCO",
    "UNIONBANK", "UNITDSPR", "UNOMINDA", "UPL", "VBL", "VEDL", "VOLTAS", "WIPRO", "YESBANK",
    "ETERNAL", "ZYDUSLIFE"
]

# Common headers for NSE requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json"
}

def get_nse_option_chain(symbol):
    """Fetch option chain data from NSE for a given stock symbol."""
    url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
    session = requests.Session()
    try:
        # Warm-up request (important to set cookies)
        session.get(f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}", headers=HEADERS, timeout=5)
        sleep(random.uniform(1, 2))

        response = session.get(url, headers=HEADERS, timeout=5)
        if response.status_code != 200:
            print(f"❌ {symbol}: Status {response.status_code}")
            return None
        if "json" not in response.headers.get("Content-Type", ""):
            print(f"⚠️ {symbol}: Non-JSON response")
            return None

        data = response.json()
        records = data.get("records", {}).get("data", [])
        combined_data = []
        for entry in records:
            strike_price = entry.get("strikePrice", 0)
            expiry = entry.get("expiryDate", "NA")
            ce = entry.get("CE", {})
            pe = entry.get("PE", {})
            combined_data.append([
                symbol, expiry, strike_price,
                ce.get("bidprice", 0), ce.get("bidQty", 0), ce.get("askPrice", 0), ce.get("askQty", 0),
                pe.get("bidprice", 0), pe.get("bidQty", 0), pe.get("askPrice", 0), pe.get("askQty", 0)
            ])
        return pd.DataFrame(combined_data, columns=[
            "Symbol", "Expiry", "Strike Price",
            "Call Bid Price", "Call Bid Qty", "Call Ask Price", "Call Ask Qty",
            "Put Bid Price", "Put Bid Qty", "Put Ask Price", "Put Ask Qty"
        ])
    except requests.exceptions.RequestException as e:
        print(f"‼️ {symbol}: {e}")
        return None

# Run parallel fetch
all_data = pd.DataFrame()
with ThreadPoolExecutor(max_workers=8) as executor:
    future_to_symbol = {executor.submit(get_nse_option_chain, symbol): symbol for symbol in symbols}
    for future in as_completed(future_to_symbol):
        symbol = future_to_symbol[future]
        try:
            df = future.result()
            if df is not None and not df.empty:
                all_data = pd.concat([all_data, df], ignore_index=True)
                print(f"✅ Data added for {symbol}")
            else:
                print(f"⚠️ Skipped {symbol}")
        except Exception as e:
            print(f"‼️ Error {symbol}: {e}")

# Save
if not all_data.empty:
    all_data.to_csv("All_Option_Chain_Data.csv", index=False)
    print("🔥 All data saved in 'All_Option_Chain_Data.csv'")
else:
    print("❌ No data fetched.")

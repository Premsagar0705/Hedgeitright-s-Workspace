import requests
import pandas as pd
import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

# Mapping: display name → NSE symbol
symbol_map = {
    "AARTIIND": "AARTIIND", "ABFRL": "ABFRL", "ACC": "ACC", "ADANIENT": "ADANIENT",
    "ADANIGREEN": "ADANIGREEN", "ADANIPORTS": "ADANIPORTS", "Ashok Leyland": "ASHOKLEY",
    "AMBUJACEM": "AMBUJACEM", "APOLLOHOSP": "APOLLOHOSP", "ASIANPAINT": "ASIANPAINT",
    "ATGL": "ATGL", "Axis bank": "AXISBANK", "BAJAJ-AUTO": "BAJAJ-AUTO",
    "BAJAJFINSV": "BAJAJFINSV", "Balkrishna Industries": "BALKRISIND",
    "Bandhan bank": "BANDHANBNK", "Bank of Baroda": "BANKBARODA", "BEL": "BEL",
    "Bharat Forage": "BHARATFORG", "BHARTIARTL": "BHARTIARTL", "Bhel": "BHEL", "BPCL": "BPCL",
    "Birla soft": "BSOFT", "Cesc": "CESC", "Chambal fertilizer": "CHAMBLFERT", "CIPLA": "CIPLA",
    "Container corporation": "CONCOR", "Crompton greaves": "CROMPTON", "Dabur": "DABUR",
    "Delhivery": "DELHIVERY", "DLF": "DLF", "DRREDDY": "DRREDDY", "Eicher motors": "EICHERMOT",
    "Exide industries": "EXIDEIND", "Federal bank": "FEDERALBNK", "GAIL": "GAIL",
    "Granules India": "GRANULES", "GRASIM": "GRASIM", "HCLTECH": "HCLTECH", "HDFCBANK": "HDFCBANK",
    "HDFCLIFE": "HDFCLIFE", "HEROMOTOCO": "HEROMOTOCO", "HINDALCO": "HINDALCO",
    "HINDCOPPER": "HINDCOPPER", "HINDUNILVR": "HINDUNILVR", "Hindustan zinc": "HINDZINC",
    "Hudco": "HUDCO", "ICICIBANK": "ICICIBANK", "ICICI Prudential": "ICICIPRULI",
    "Idea": "IDEA", "IEX": "IEX", "IGL": "IGL", "INDHOTEL": "INDHOTEL", "INDUSINDBK": "INDUSINDBK",
    "Indus tower": "INDUSTOWER", "INFY": "INFY", "IOC": "IOC", "IRCTC": "IRCTC", "Irfc": "IRFC",
    "ITC": "ITC", "JIOFIN": "JIOFIN", "JSWSTEEL": "JSWSTEEL", "Kalyan jeweller": "KALYANKJIL",
    "KOTAKBANK": "KOTAKBANK", "Laurus labs": "LAURUSLABS", "LIC housing finance": "LICHSGFIN",
    "LT": "LT", "LT Finance": "LTF", "M&M": "M%26M", "M&M Finance": "M%26MFIN", "MANAPPURAM": "MANAPPURAM",
    "Marico": "MARICO", "MARUTI": "MARUTI", "MGL": "MGL", "NATIONALUM": "NATIONALUM",
    "NCC": "NCC", "NESTLEIND": "NESTLEIND", "NMDC": "NMDC", "NTPC": "NTPC", "Oberoi reality": "OBEROIRLTY",
    "ONGC": "ONGC", "PETRONET": "PETRONET", "PFC": "PFC", "PNB": "PNB", "POWERGRID": "POWERGRID",
    "Rail Vikas Nigam": "RVNL", "Rbl bank": "RBLBANK", "REC": "RECLTD", "Reliance": "RELIANCE",
    "SAIL": "SAIL", "SBILIFE": "SBILIFE", "SBIN": "SBIN", "SHRIRAMFIN": "SHRIRAMFIN", "SUNPHARMA": "SUNPHARMA",
    "TATACONSUM": "TATACONSUM", "Tata motors": "TATAMOTORS", "TATAPOWER": "TATAPOWER",
    "TATASTEEL": "TATASTEEL", "TCS": "TCS", "TECHM": "TECHM", "TITAN": "TITAN", "TRENT": "TRENT",
    "ULTRACEMCO": "ULTRACEMCO", "UPL": "UPL", "VEDL": "VEDL", "Wipro": "WIPRO", "Yesbank": "YESBANK",
    "ETERNAL": "ETERNAL"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def get_nse_option_chain(symbol, display_name):
    url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
    session = requests.Session()
    try:
        # Warm up cookies
        session.get(f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}", headers=HEADERS, timeout=5)
        sleep(random.uniform(1, 2))
        
        response = session.get(url, headers=HEADERS, timeout=5)
        if response.status_code != 200 or "json" not in response.headers.get("Content-Type", ""):
            print(f"❌ Invalid response for {display_name}")
            return None

        data = response.json()
        records = data.get("records", {}).get("data", [])
        combined_data = []

        for entry in records:
            strike_price = entry.get("strikePrice")
            expiry = entry.get("expiryDate")
            ce = entry.get("CE", {})
            pe = entry.get("PE", {})

            combined_data.append([
                display_name, expiry, strike_price,
                ce.get("bidprice", 0), ce.get("bidQty", 0), ce.get("askPrice", 0), ce.get("askQty", 0),
                pe.get("bidprice", 0), pe.get("bidQty", 0), pe.get("askPrice", 0), pe.get("askQty", 0)
            ])

        return pd.DataFrame(combined_data, columns=[
            "Company", "Expiry", "Strike Price",
            "Call Bid ", "Call Qty", "Call Ask ", "Call Qty",
            "Put Bid ", "Put Qty", "Put Ask ", "Put Qty"
        ])

    except requests.exceptions.RequestException as e:
        print(f"‼️ Error fetching {display_name}: {e}")
        return None

# Run in parallel
all_data = pd.DataFrame()

with ThreadPoolExecutor(max_workers=10) as executor:
    future_map = {
        executor.submit(get_nse_option_chain, nse_symbol, name): name
        for name, nse_symbol in symbol_map.items()
    }

    for future in as_completed(future_map):
        name = future_map[future]
        try:
            df = future.result()
            if df is not None and not df.empty:
                all_data = pd.concat([all_data, df], ignore_index=True)
                print(f"✅ Data fetched for {name}")
            else:
                print(f"⚠️ No data for {name}")
        except Exception as e:
            print(f"‼️ Exception while processing {name}: {e}")

# Save output
if not all_data.empty:
    all_data.to_csv("All_Option_Chain_Data.csv", index=False)
    print("🔥 Data saved to All_Option_Chain_Data.csv")
else:
    print("❌ No data to save.")

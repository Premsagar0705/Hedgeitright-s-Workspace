import requests
import pandas as pd
import time

def fetch_live_option_chain(symbol):
    url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}",
        "Connection": "keep-alive"
    }

    session = requests.Session()
    session.headers.update(headers)

    # Try up to 5 times if NSE blocks
    for attempt in range(5):
        try:
            # Step 1: Get cookies
            session.get("https://www.nseindia.com", timeout=5)

            # Step 2: Fetch option chain
            response = session.get(url, timeout=10)
            if "json" not in response.headers.get("Content-Type", ""):
                print(f"Attempt {attempt+1}: NSE blocked {symbol}, retrying...")
                time.sleep(2 + attempt)  # increasing delay
                continue

            data = response.json()
            records = []
            for item in data["records"]["data"]:
                for cepe in ["CE", "PE"]:
                    if cepe in item:
                        row = item[cepe]
                        row["type"] = cepe
                        row["underlying"] = symbol
                        row["expiryDate"] = item.get("expiryDate", "")
                        records.append(row)

            return pd.DataFrame(records)

        except Exception as e:
            print(f"Attempt {attempt+1} failed for {symbol}: {e}")
            time.sleep(2)

    print(f"Failed to fetch live data for {symbol}")
    return pd.DataFrame()

# --- Example usage ---
symbols = ["APOLLOTYRE", "RELIANCE", "TCS"]
all_data = []

for sym in symbols:
    print(f"Fetching live option chain for {sym}")
    df = fetch_live_option_chain(sym)
    if not df.empty:
        all_data.append(df)
    time.sleep(2)  # small delay to reduce blocking

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_excel("live_option_chain.xlsx", index=False)
    print("Saved live option chain to live_option_chain.xlsx")
else:
    print("No data fetched.")

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# List of F&O stock symbols from NSE (you can modify or add more symbols if needed)
stocks = [
    "ACC.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ATUL.NS", "BALKRISIND.NS", "BATAINDIA.NS", 
    "BERGEPAINT.NS", "BHARATFORG.NS", "ABBOTINDIA.NS", "BRITANNIA.NS", "EXIDEIND.NS", "CIPLA.NS", 
    "COLPAL.NS", "COROMANDEL.NS", "DEEPAKNTR.NS", "EICHERMOT.NS", "ESCORTS.NS", "NIFTY_FIN_SERVICE.NS", "NESTLEIND.NS", "^NSEBANK", 
    "GNFC.NS", "AMBUJACEM.NS", "GRASIM.NS", "HDFCBANK.NS", "HEROMOTOCO.NS", "ABB.NS", "HINDALCO.NS", "HINDUNILVR.NS", 
    "INDIACEM.NS", "INDHOTEL.NS", "ITC.NS", "CUMMINSIND.NS", "TRENT.NS", "LT.NS", "RAMCOCEM.NS", "M&M.NS", 
    "MFSL.NS", "BOSCHLTD.NS", "MRF.NS", "PEL.NS", "RELIANCE.NS", "VEDL.NS", "SHREECEM.NS", "SRF.NS", 
    "SIEMENS.NS", "TATACHEM.NS", "TATAPOWER.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", 
    "VOLTAS.NS", "WIPRO.NS", "APOLLOHOSP.NS", "DRREDDY.NS", "TITAN.NS", "CANFINHOME.NS", "SBIN.NS", 
    "SHRIRAMFIN.NS", "CHOLAFIN.NS", "BALRAMCHIN.NS", "BPCL.NS", "TATACOMM.NS", "BEL.NS", "SAIL.NS", 
    "NATIONALUM.NS", "HINDPETRO.NS", "BHEL.NS", "KOTAKBANK.NS", "AARTIIND.NS", "UPL.NS", "PIIND.NS", "INFY.NS", 
    "MSUMI.NS", "LUPIN.NS", "CHAMBLFERT.NS", "ZEEL.NS", "PIDILITIND.NS", "HAVELLS.NS", "MPHASIS.NS", 
    "DABUR.NS", "TORNTPHARM.NS", "IPCALAB.NS", "FEDERALBNK.NS", "BAJFINANCE.NS", "HINDCOPPER.NS", 
    "ADANIENT.NS", "LICHSGFIN.NS", "SUNPHARMA.NS", "AUROPHARMA.NS", "JSWSTEEL.NS", "HDFCBANK.NS", "TCS.NS", 
    "ICICIBANK.NS", "POWERGRID.NS", "BANKBARODA.NS", "CANBK.NS", "MARUTI.NS", "INDUSINDBK.NS", "AXISBANK.NS", 
    "HCLTECH.NS", "RBLBANK.NS", "ONGC.NS", "MANAPPURAM.NS", "DLF.NS", "CUB.NS", "PNB.NS", "TVSMOTOR.NS", 
    "UNITDSPR.NS", "NTPC.NS", "IOC.NS", "COALINDIA.NS", "HAL.NS", "NMDC.NS", "PFC.NS", "GAIL.NS", 
    "PAGEIND.NS", "MARICO.NS", "CONCOR.NS", "GRANULES.NS", "OFSS.NS", "MGL.NS", "JUBLFOOD.NS", "PVRINOX.NS", 
    "BIOCON.NS", "SUNTV.NS", "BHARTIARTL.NS", "GODREJPROP.NS", "BSOFT.NS", "M&MFIN.NS", "JKCEMENT.NS", 
    "DELTACORP.NS", "TECHM.NS", "RECLTD.NS", "LTIM.NS", "PERSISTENT.NS", "NAUKRI.NS", "ALKEM.NS", 
    "PETRONET.NS", "SBICARD.NS", "JINDALSTEL.NS", "^NSEI", "GLENMARK.NS", "IGL.NS", "ZYDUSLIFE.NS", 
    "DIVISLAB.NS", "HDFCAMC.NS", "ADANIPORTS.NS", "GODREJCP.NS", "HDFCLIFE.NS", "ICICIPRULI.NS", 
    "SBILIFE.NS", "ICICIGI.NS", "GMRAIRPORT.NS", "IDEA.NS", "UBL.NS", "IRCTC.NS", "NAVINFLUOR.NS", 
    "MUTHOOTFIN.NS", "ULTRACEMCO.NS", "COFORGE.NS", "MCX.NS", "SYNGENE.NS", "POLYCAB.NS", "ASTRAL.NS", 
    "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "INDIGO.NS", "AUBANK.NS", "DIXON.NS", "SAMMAANCAP.NS", "OBEROIRLTY.NS", 
    "INDUSTOWER.NS", "ABCAPITAL.NS", "ABFRL.NS", "LTF.NS", "LALPATHLAB.NS", "GUJGASLTD.NS", 
    "LTTS.NS", "LAURUSLABS.NS", "IDFCFIRSTB.NS", "INTELLECT.NS", "METROPOLIS.NS", "CROMPTON.NS", 
    "BANDHANBNK.NS", "INDIAMART.NS", "DALBHARAT.NS", "IEX.NS", "^NSMIDCP", "NIFTY_MID_SELECT.NS"
]
# Calculate start date for 10 years ago
start_date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

# Create Excel writer
with pd.ExcelWriter("fno_stocks_data_past_10_years.xlsx", engine="openpyxl") as writer:
    for stock in stocks:
        try:
            print(f"✅ Downloading data for {stock}...")
            
            # Explicitly set auto_adjust to avoid FutureWarning
            stock_data = yf.download(
                stock,
                start=start_date,
                end=end_date,
                interval="1d",
                auto_adjust=True  # Set to False if you want raw data
            )

            if not stock_data.empty:
                # Sheet name limitation: 31 characters max
                sheet_name = stock.replace(".NS", "")[:31]
                stock_data.to_excel(writer, sheet_name=sheet_name)
            else:
                print(f"⚠️ No data found for {stock}.")
        
        except Exception as e:
            print(f"❌ Failed to download data for {stock}: {e}")

print("🔥 Download complete! Data saved to fno_stocks_data_past_10_years.xlsx.")

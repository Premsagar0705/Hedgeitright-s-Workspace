import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# List of tickers (cleaned and deduplicated)
stocks = [
    "ABBINDIA.NS", "ACC.NS", "APLAPOLLO.NS", "AUBANK.NS", "AARTIIND.NS", "ADANIENSOL.NS", "ADANIENT.NS",
    "ADANIGREEN.NS", "ADANIPORTS.NS", "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS", "AMBUJACEM.NS",
    "ANGELONE.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS",
    "AUROPHARMA.NS", "DMART.NS", "AXISBANK.NS", "BSOFT.NS", "BSE.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS",
    "BAJAJFINSV.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "BERGEPAINT.NS",
    "BEL.NS", "BHARATFORG.NS", "BHEL.NS", "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BOSCHLTD.NS",
    "BRITANNIA.NS", "CESC.NS", "CGPOWER.NS", "CANBK.NS", "CDSL.NS", "CHAMBLFERT.NS", "CHOLAFIN.NS",
    "CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CAMS.NS", "CONCOR.NS", "CROMPTON.NS",
    "CUMMINSIND.NS", "CYIENT.NS", "DLF.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DELHIVERY.NS",
    "DIVISLAB.NS", "DIXON.NS", "DRREDDY.NS", "ETERNAL.NS", "EICHERMOT.NS", "ESCORTS.NS", "EXIDEIND.NS",
    "NYKAA.NS", "GAIL.NS", "GMRAIRPORT.NS", "GLENMARK.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRANULES.NS",
    "GRASIM.NS", "HCLTECH.NS", "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HFCL.NS", "HAVELLS.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HAL.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HINDUNILVR.NS",
    "HINDZINC.NS", "HUDCO.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDFCFIRSTB.NS",
    "IIFL.NS", "IRB.NS", "ITC.NS", "INDIANB.NS", "IEX.NS", "IOC.NS", "IRCTC.NS", "IRFC.NS", "IREDA.NS",
    "IGL.NS", "INDUSTOWER.NS", "INDUSINDBK.NS", "NAUKRI.NS", "INFY.NS", "INOXWIND.NS", "INDIGO.NS",
    "JSWENERGY.NS", "JSWSTEEL.NS", "JSL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "JUBLFOOD.NS", "KEI.NS",
    "KPITTECH.NS", "KALYANKJIL.NS", "KOTAKBANK.NS", "LTF.NS", "LICHSGFIN.NS", "LTIM.NS", "LT.NS",
    "LAURUSLABS.NS", "LICI.NS", "LUPIN.NS", "MRF.NS", "LODHA.NS", "MGL.NS", "M&MFIN.NS", "M&M.NS",
    "MANAPPURAM.NS", "MARICO.NS", "MARUTI.NS", "MFSL.NS", "MAXHEALTH.NS", "MPHASIS.NS", "MCX.NS",
    "MUTHOOTFIN.NS", "NBCC.NS", "NCC.NS", "NHPC.NS", "NMDC.NS", "NTPC.NS", "NATIONALUM.NS",
    "NESTLEIND.NS", "OBEROIRLTY.NS", "ONGC.NS", "OIL.NS", "PAYTM.NS", "OFSS.NS", "POLICYBZR.NS",
    "PIIND.NS", "PNBHOUSING.NS", "PAGEIND.NS", "PATANJALI.NS", "PERSISTENT.NS", "PETRONET.NS",
    "PIDILITIND.NS", "PEL.NS", "POLYCAB.NS", "POONAWALLA.NS", "PFC.NS", "POWERGRID.NS", "PRESTIGE.NS",
    "PNB.NS", "RBLBANK.NS", "RECLTD.NS", "RELIANCE.NS", "SBICARD.NS", "SBILIFE.NS", "SHREECEM.NS",
    "SJVN.NS", "SRF.NS", "MOTHERSON.NS", "SHRIRAMFIN.NS", "SIEMENS.NS", "SOLARINDS.NS", "SONACOMS.NS",
    "SBIN.NS", "SAIL.NS", "SUNPHARMA.NS", "SUPREMEIND.NS", "SYNGENE.NS", "TATACONSUM.NS", "TITAGARH.NS",
    "TVSMOTOR.NS", "TATACHEM.NS", "TATACOMM.NS", "TCS.NS", "TATAELXSI.NS", "TATAMOTORS.NS",
    "TATAPOWER.NS", "TATASTEEL.NS", "TATATECH.NS", "TECHM.NS", "FEDERALBNK.NS", "INDHOTEL.NS",
    "PHOENIXLTD.NS", "RAMCOCEM.NS", "TITAN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS",
    "TIINDIA.NS", "UPL.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "UNITDSPR.NS", "VBL.NS", "VEDL.NS",
    "IDEA.NS", "VOLTAS.NS", "WIPRO.NS", "YESBANK.NS", "ZYDUSLIFE.NS", "ATUL.NS", "BATAINDIA.NS",
    "ABBOTINDIA.NS", "COROMANDEL.NS", "NIFTY_FIN_SERVICE.NS", "^NSEBANK", "GNFC.NS", "ABB.NS",
    "INDIACEM.NS", "CANFINHOME.NS", "BALRAMCHIN.NS", "MSUMI.NS", "ZEEL.NS", "IPCALAB.NS", "CUB.NS",
    "PVRINOX.NS", "SUNTV.NS", "JKCEMENT.NS", "DELTACORP.NS", "^NSEI", "UBL.NS", "NAVINFLUOR.NS",
    "SAMMAANCAP.NS", "LALPATHLAB.NS", "GUJGASLTD.NS", "LTTS.NS", "INTELLECT.NS", "METROPOLIS.NS",
    "INDIAMART.NS", "^NSMIDCP", "NIFTY_MID_SELECT.NS", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "NIFTYNXT50.NS"
]

# Calculate the start date for 10 years ago
start_date = (datetime.now() - timedelta(days=365*10)).strftime('%Y-%m-%d')

# Create an Excel writer to store multiple stock data in one Excel file
with pd.ExcelWriter("stocks_data_past_10_years_Tillnow.xlsx", engine="openpyxl") as writer:
    for stock in stocks:
        try:
            # Download historical data for the last 10 years, including up to the current date
            print(f"✅Downloading data for {stock}...")
            stock_data = yf.download(stock, start=start_date, interval="1d", auto_adjust=True)

            # Save the data to Excel (one sheet per stock)
            stock_data.to_excel(writer, sheet_name=stock.split('.')[0][:30])  # Sheet names can't be longer than 31 chars
        except Exception as e:
            print(f"❌Failed to download data for {stock}: {e}")

print("🔥Download complete! Data saved to stocks_data_past_10_years_Tillnow.xlsx.")

#Failed downloads:['BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY', 'ABBINDIA.NS', 'NIFTY_MID_SELECT.NS','NIFTYNXT50.NS']
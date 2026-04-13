import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import SYMBOL_1, SYMBOL_2


def get_data():

    print("Downloading ETF data...")

    end_date = datetime.today()
    start_date = end_date - timedelta(days=5 * 365)

    nifty = yf.download(
        SYMBOL_1,
        start=start_date,
        end=end_date,
        progress=False
    )

    bank = yf.download(
        SYMBOL_2,
        start=start_date,
        end=end_date,
        progress=False
    )

    if nifty.empty:
        raise ValueError(f"Failed to download data for {SYMBOL_1}")

    if bank.empty:
        raise ValueError(f"Failed to download data for {SYMBOL_2}")

    # Extract Close prices only
    nifty_close = nifty["Close"]
    bank_close = bank["Close"]

    # Align both datasets on same dates
    data = pd.concat(
        [nifty_close, bank_close],
        axis=1,
        join="inner"
    )

    data.columns = ["NIFTY", "BANK"]

    data.dropna(inplace=True)

    return data
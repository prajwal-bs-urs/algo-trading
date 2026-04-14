import yfinance as yf
import pandas as pd


def download(symbol):

    print(f"Downloading {symbol}...")

    df = yf.download(symbol, period="10y", progress=False)

    if df.empty:
        raise ValueError(f"Failed to download {symbol}")

    return df["Close"]


def get_data():

    print("Downloading index data...")

    nifty = download("^NSEI")
    bank = download("^NSEBANK")
    midcap = download("^NSEMDCP50")
    gold = download("GC=F")
    usdinr = download("INR=X")

    data = pd.concat(
        [nifty, bank, midcap, gold, usdinr],
        axis=1
    )

    data.columns = [
        "NIFTY",
        "BANK",
        "MIDCAP",
        "GOLD",
        "USDINR"
    ]

    data.dropna(inplace=True)

    print("Dataset length (years):", len(data) / 252)

    return data
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


def get_data_range(start_date: str, end_date: str) -> pd.DataFrame:
    """Download NIFTY and BANK data for a specific date range.

    Used by walk-forward analysis to slice history into windows.
    """
    nifty = yf.download("^NSEI", start=start_date, end=end_date, progress=False)
    bank = yf.download("^NSEBANK", start=start_date, end=end_date, progress=False)

    data = pd.concat(
        [nifty["Close"], bank["Close"]],
        axis=1,
        join="inner",
    )
    data.columns = ["NIFTY", "BANK"]
    data.dropna(inplace=True)

    return data

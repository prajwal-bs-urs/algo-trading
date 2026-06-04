from datetime import datetime
import pandas as pd

from config import INITIAL_CAPITAL
from data_loader import get_data_range
from performance_metrics import calculate_max_drawdown


def run_backtest(data, window):
    data["RS"] = data["BANK"] / data["NIFTY"]

    data["RS_MA"] = data["RS"].rolling(window).mean()

    data["NIFTY_MA"] = data["NIFTY"].rolling(window).mean()

    data["BANK_MA"] = data["BANK"].rolling(window).mean()

    data["Signal"] = 0

    data.loc[
        (data["RS"] > data["RS_MA"]) &
        (data["BANK"] > data["BANK_MA"]),
        "Signal"
    ] = 2

    data.loc[
        (data["RS"] < data["RS_MA"]) &
        (data["NIFTY"] > data["NIFTY_MA"]),
        "Signal"
    ] = 1

    capital = INITIAL_CAPITAL
    position = None
    units = 0

    equity_curve = []

    for _, row in data.iterrows():

        signal = row["Signal"]

        nifty_price = row["NIFTY"]
        bank_price = row["BANK"]

        if signal == 1:

            if position == "BANK":
                capital = units * bank_price
                units = 0

            if position != "NIFTY":
                units = capital / nifty_price
                capital = 0
                position = "NIFTY"


        elif signal == 2:

            if position == "NIFTY":
                capital = units * nifty_price
                units = 0

            if position != "BANK":
                units = capital / bank_price
                capital = 0
                position = "BANK"


        else:

            if position == "NIFTY":

                capital = units * nifty_price
                units = 0
                position = None

            elif position == "BANK":

                capital = units * bank_price
                units = 0
                position = None

        if position == "NIFTY":

            portfolio_value = units * nifty_price

        elif position == "BANK":

            portfolio_value = units * bank_price

        else:

            portfolio_value = capital

        equity_curve.append(portfolio_value)

    final_value = equity_curve[-1]

    years = (data.index[-1] - data.index[0]).days / 365

    CAGR = ((final_value / INITIAL_CAPITAL) ** (1 / years) - 1) * 100

    max_dd = calculate_max_drawdown(equity_curve) * 100

    return CAGR, max_dd


# WALK-FORWARD WINDOWS

windows = [
    ("2016-01-01", "2020-01-01"),
    ("2018-01-01", "2022-01-01"),
    ("2020-01-01", "2024-01-01"),
]

test_window = 10

print("\nRunning walk-forward validation...\n")

for start, end in windows:
    print(f"Testing period: {start} → {end}")

    dataset = get_data_range(start, end)

    CAGR, dd = run_backtest(dataset, test_window)

    print(f"CAGR = {round(CAGR, 2)}% | Drawdown = {round(dd, 2)}%\n")

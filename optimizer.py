from data_loader import get_data
from config import INITIAL_CAPITAL
import pandas as pd


def calculate_drawdown(equity_curve):
    equity_series = pd.Series(equity_curve)

    rolling_max = equity_series.cummax()

    drawdown = (equity_series - rolling_max) / rolling_max

    return drawdown.min()


def run_backtest(window):
    data = get_data()

    # Relative strength ratio
    data["RS"] = data["BANK"] / data["NIFTY"]

    # Moving average with test window
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

    years = 5

    CAGR = ((final_value / INITIAL_CAPITAL) ** (1 / years) - 1) * 100

    max_drawdown = calculate_drawdown(equity_curve) * 100

    return CAGR, max_drawdown


print("\nRunning parameter robustness test...\n")

results = []

for window in range(10, 65, 5):
    CAGR, dd = run_backtest(window)

    results.append((window, CAGR, dd))

    print(
        f"Window={window} | CAGR={round(CAGR, 2)}% | Drawdown={round(dd, 2)}%"
    )

best = max(results, key=lambda x: x[1])

print("\nBest Window Based on CAGR:")

print(best)

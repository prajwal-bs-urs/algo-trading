from data_loader import get_data
from strategy import generate_signals
from config import INITIAL_CAPITAL

import pandas as pd
import matplotlib.pyplot as plt


def calculate_drawdown(equity_curve):
    """
    Calculates maximum drawdown from equity curve
    """

    equity_series = pd.Series(equity_curve)

    rolling_max = equity_series.cummax()

    drawdown = (equity_series - rolling_max) / rolling_max

    return drawdown.min()


def run_backtest():

    print("Running backtest...")

    data = get_data()

    data = generate_signals(data)

    capital = INITIAL_CAPITAL
    position = None
    units = 0

    equity_curve = []


    for index, row in data.iterrows():

        signal = row["Signal"]

        nifty_price = row["NIFTY"]
        bank_price = row["BANK"]


        # SWITCH TO NIFTY
        if signal == 1:

            if position == "BANK":
                capital = units * bank_price
                units = 0

            if position != "NIFTY":
                units = capital / nifty_price
                capital = 0
                position = "NIFTY"


        # SWITCH TO BANK
        elif signal == 2:

            if position == "NIFTY":
                capital = units * nifty_price
                units = 0

            if position != "BANK":
                units = capital / bank_price
                capital = 0
                position = "BANK"


        # MOVE TO CASH
        else:

            if position == "NIFTY":
                capital = units * nifty_price
                units = 0
                position = None

            elif position == "BANK":
                capital = units * bank_price
                units = 0
                position = None


        # PORTFOLIO VALUATION

        if position == "NIFTY":
            portfolio_value = units * nifty_price

        elif position == "BANK":
            portfolio_value = units * bank_price

        else:
            portfolio_value = capital


        equity_curve.append(portfolio_value)


    # FINAL METRICS

    final_value = equity_curve[-1]

    profit = final_value - INITIAL_CAPITAL

    years = 5

    CAGR = ((final_value / INITIAL_CAPITAL) ** (1 / years) - 1) * 100

    max_drawdown = calculate_drawdown(equity_curve) * 100


    # PRINT RESULTS

    print("\n========== BACKTEST RESULTS ==========")

    print("Initial Capital:", INITIAL_CAPITAL)

    print("Final Capital:", round(final_value, 2))

    print("Profit:", round(profit, 2))

    print("Return %:", round((profit / INITIAL_CAPITAL) * 100, 2))

    print("CAGR:", round(CAGR, 2), "%")

    print("Max Drawdown:", round(max_drawdown, 2), "%")


    # EQUITY CURVE PLOT

    plt.figure(figsize=(12, 6))

    plt.plot(equity_curve)

    plt.title("Strategy Equity Curve")

    plt.xlabel("Trading Days")

    plt.ylabel("Portfolio Value")

    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    run_backtest()
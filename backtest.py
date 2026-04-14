from data_loader import get_data
from strategy import generate_signals
from config import INITIAL_CAPITAL
from performance_metrics import generate_performance_report
from benchmark_comparison import benchmark_report

import pandas as pd
import matplotlib.pyplot as plt


TRANSITION_COST = 0.002


def calculate_drawdown(equity_curve):

    equity_series = pd.Series(equity_curve)

    rolling_max = equity_series.cummax()

    drawdown = (equity_series - rolling_max) / rolling_max

    return drawdown.min()


def signal_to_position(signal):

    if signal == 1:
        return "NIFTY"

    elif signal == 2:
        return "BANK"

    elif signal == 3:
        return "MIDCAP"

    elif signal == 4:
        return "GOLD"

    elif signal == 5:
        return "USDINR"

    return None


def run_backtest():

    print("Running realistic execution backtest...")

    data = get_data()

    print("Dataset length (years):", len(data) / 252)

    data = generate_signals(data)

    capital = INITIAL_CAPITAL
    position = None
    units = 0

    trade_count = 0

    equity_curve = []

    for _, row in data.iterrows():

        signal = row["Signal"]

        target_position = signal_to_position(signal)

        nifty_price = row["NIFTY"]
        bank_price = row["BANK"]
        midcap_price = row["MIDCAP"]
        gold_price = row["GOLD"]
        usdinr_price = row["USDINR"]

        # =============================
        # Position switching logic
        # =============================

        if target_position != position:

            # Exit current position

            if position == "NIFTY":

                capital = units * nifty_price

            elif position == "BANK":

                capital = units * bank_price

            elif position == "MIDCAP":

                capital = units * midcap_price

            elif position == "GOLD":

                capital = units * gold_price

            elif position == "USDINR":

                capital = units * usdinr_price

            units = 0

            # Apply transition cost once

            capital *= (1 - TRANSITION_COST)

            # Enter new position

            if target_position == "NIFTY":

                units = capital / nifty_price
                capital = 0

            elif target_position == "BANK":

                units = capital / bank_price
                capital = 0

            elif target_position == "MIDCAP":

                units = capital / midcap_price
                capital = 0

            elif target_position == "GOLD":

                units = capital / gold_price
                capital = 0

            elif target_position == "USDINR":

                units = capital / usdinr_price
                capital = 0

            position = target_position

            trade_count += 1

        # =============================
        # Portfolio valuation
        # =============================

        if position == "NIFTY":

            portfolio_value = units * nifty_price

        elif position == "BANK":

            portfolio_value = units * bank_price

        elif position == "MIDCAP":

            portfolio_value = units * midcap_price

        elif position == "GOLD":

            portfolio_value = units * gold_price

        elif position == "USDINR":

            portfolio_value = units * usdinr_price

        else:

            portfolio_value = capital

        equity_curve.append(portfolio_value)

    final_value = equity_curve[-1]

    profit = final_value - INITIAL_CAPITAL

    years = len(data) / 252

    CAGR = ((final_value / INITIAL_CAPITAL) ** (1 / years) - 1) * 100

    max_drawdown = calculate_drawdown(equity_curve) * 100

    print("\n========== REALISTIC BACKTEST RESULTS ==========")

    print("Initial Capital:", INITIAL_CAPITAL)

    print("Final Capital:", round(final_value, 2))

    print("Profit:", round(profit, 2))

    print("Return %:", round((profit / INITIAL_CAPITAL) * 100, 2))

    print("CAGR:", round(CAGR, 2), "%")

    print("Max Drawdown:", round(max_drawdown, 2), "%")

    print("Total transitions:", trade_count)

    generate_performance_report(equity_curve)

    benchmark_report(equity_curve, data["NIFTY"])

    # =============================
    # Plot equity curve
    # =============================

    plt.plot(equity_curve)

    plt.title("Equity Curve (Macro Tactical Allocation)")

    plt.xlabel("Days")

    plt.ylabel("Portfolio Value")

    plt.show()


if __name__ == "__main__":

    run_backtest()

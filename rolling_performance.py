import pandas as pd

from data_loader import get_data
from strategy import generate_signals


INITIAL_CAPITAL = 100000

TRANSITION_COST = 0.002


def signal_to_position(signal):

    if signal == 1:
        return "NIFTY"

    elif signal == 2:
        return "BANK"

    return None


def rolling_test(window_years=2):

    print(f"\nRunning rolling {window_years}-year stability test...\n")

    data = get_data()

    data = generate_signals(data)

    trading_days = 252
    window_size = window_years * trading_days

    results = []

    for start in range(len(data) - window_size):

        subset = data.iloc[start:start + window_size]

        capital = INITIAL_CAPITAL

        position = None
        units = 0

        for i in range(len(subset)):

            row = subset.iloc[i]

            signal = row["Signal"]

            target_position = signal_to_position(signal)

            nifty_price = row["NIFTY"]
            bank_price = row["BANK"]


            if target_position != position:

                if position == "NIFTY":

                    capital = units * nifty_price
                    units = 0

                elif position == "BANK":

                    capital = units * bank_price
                    units = 0


                capital *= (1 - TRANSITION_COST)


                if target_position == "NIFTY":

                    units = capital / nifty_price
                    capital = 0

                elif target_position == "BANK":

                    units = capital / bank_price
                    capital = 0


                position = target_position


        if position == "NIFTY":

            capital = units * subset.iloc[-1]["NIFTY"]

        elif position == "BANK":

            capital = units * subset.iloc[-1]["BANK"]


        CAGR = ((capital / INITIAL_CAPITAL) **
                (1 / window_years) - 1) * 100

        results.append(CAGR)


    print("Rolling performance summary:\n")

    print("Minimum CAGR:", round(min(results), 2), "%")

    print("Maximum CAGR:", round(max(results), 2), "%")

    print("Average CAGR:", round(sum(results) / len(results), 2), "%")


if __name__ == "__main__":

    rolling_test(window_years=2)
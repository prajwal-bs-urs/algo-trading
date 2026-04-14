import pandas as pd

from data_loader import get_data
from strategy import generate_signals


def analyze_trade_frequency():

    data = get_data()

    data = generate_signals(data)

    data["Switch"] = data["Signal"].diff().abs()

    switches = data[data["Switch"] > 0]

    switches_per_year = switches.groupby(
        switches.index.year
    ).size()

    avg_switches = switches_per_year.mean()

    print("\nSwitches per year:\n")
    print(switches_per_year)

    print("\nAverage switches per year:", round(avg_switches, 2))


if __name__ == "__main__":

    analyze_trade_frequency()
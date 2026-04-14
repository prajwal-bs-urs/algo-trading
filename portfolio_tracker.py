from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

from data_loader import get_data
from strategy import generate_signals
from telegram_alert import send_message, send_photo


LOG_FILE = "portfolio_log.csv"
CHART_FILE = "equity_curve.png"

INITIAL_CAPITAL = 500000


SIGNAL_MAP = {

    0: "CASH",
    1: "NIFTYBEES",
    2: "BANKBEES",
    3: "GOLDBEES",
    4: "LIQUIDBEES"

}


def update_portfolio():

    today = datetime.today().strftime("%Y-%m-%d")

    data = get_data()

    data = generate_signals(data)

    today_signal = int(data.iloc[-1]["Signal"])

    today_asset = SIGNAL_MAP[today_signal]

    today_row = data.iloc[-1]
    yesterday_row = data.iloc[-2]


    # Prices

    nifty_today = today_row["NIFTY"]
    nifty_yesterday = yesterday_row["NIFTY"]

    bank_today = today_row["BANK"]
    bank_yesterday = yesterday_row["BANK"]

    gold_today = today_row["GOLD"]
    gold_yesterday = yesterday_row["GOLD"]

    liquid_today = today_row["LIQUID"]
    liquid_yesterday = yesterday_row["LIQUID"]


    # Load previous portfolio

    if os.path.exists(LOG_FILE):

        df = pd.read_csv(LOG_FILE)

        last_asset = df.iloc[-1]["Allocation"]

        last_value = df.iloc[-1]["Portfolio_Value"]

        benchmark_value = df.iloc[-1]["Benchmark_Value"]

    else:

        df = pd.DataFrame(columns=[

            "Date",
            "Allocation",
            "Action",
            "Portfolio_Value",
            "Benchmark_Value"

        ])

        last_asset = None

        last_value = INITIAL_CAPITAL

        benchmark_value = INITIAL_CAPITAL


    # Detect switch

    if last_asset == today_asset:

        action = "HOLD"

    else:

        action = "SWITCH"


    # Update strategy portfolio value

    new_value = last_value


    if last_asset == "NIFTYBEES":

        daily_return = (nifty_today - nifty_yesterday) / nifty_yesterday

        new_value *= (1 + daily_return)


    elif last_asset == "BANKBEES":

        daily_return = (bank_today - bank_yesterday) / bank_yesterday

        new_value *= (1 + daily_return)


    elif last_asset == "GOLDBEES":

        daily_return = (gold_today - gold_yesterday) / gold_yesterday

        new_value *= (1 + daily_return)


    elif last_asset == "LIQUIDBEES":

        daily_return = (liquid_today - liquid_yesterday) / liquid_yesterday

        new_value *= (1 + daily_return)


    # Benchmark update (always NIFTY)

    benchmark_return = (nifty_today - nifty_yesterday) / nifty_yesterday

    benchmark_value *= (1 + benchmark_return)


    new_entry = pd.DataFrame([{

        "Date": today,

        "Allocation": today_asset,

        "Action": action,

        "Portfolio_Value": round(new_value, 2),

        "Benchmark_Value": round(benchmark_value, 2)

    }])


    df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(LOG_FILE, index=False)


    # Generate comparison chart

    plt.figure(figsize=(10, 5))

    plt.plot(df["Portfolio_Value"], label="Strategy")

    plt.plot(df["Benchmark_Value"], label="NIFTY Benchmark")

    plt.title("Strategy vs Benchmark")

    plt.xlabel("Days")

    plt.ylabel("Portfolio Value (₹)")

    plt.legend()

    plt.grid(True)

    plt.savefig(CHART_FILE)

    plt.close()


    message = f"""
📊 Portfolio Update

Date: {today}

Allocation: {today_asset}

Action: {action}

Portfolio Value: ₹{round(new_value, 2)}

Benchmark Value: ₹{round(benchmark_value, 2)}
"""


    print(message)

    send_message(message)

    send_photo(CHART_FILE)


if __name__ == "__main__":

    update_portfolio()
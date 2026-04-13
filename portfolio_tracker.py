from datetime import datetime
import os
import pandas as pd

from data_loader import get_data
from strategy import generate_signals
from telegram_alert import send_message


LOG_FILE = "portfolio_log.csv"

INITIAL_CAPITAL = 500000


SIGNAL_MAP = {
    0: "CASH",
    1: "NIFTYBEES",
    2: "BANKBEES"
}


def update_portfolio():

    today = datetime.today().strftime("%Y-%m-%d")

    data = get_data()

    data = generate_signals(data)

    today_signal = int(data.iloc[-1]["Signal"])
    today_asset = SIGNAL_MAP[today_signal]

    today_row = data.iloc[-1]
    yesterday_row = data.iloc[-2]

    nifty_today = today_row["NIFTY"]
    nifty_yesterday = yesterday_row["NIFTY"]

    bank_today = today_row["BANK"]
    bank_yesterday = yesterday_row["BANK"]


    if os.path.exists(LOG_FILE):

        df = pd.read_csv(LOG_FILE)

        last_asset = df.iloc[-1]["Allocation"]
        last_value = df.iloc[-1]["Portfolio_Value"]

    else:

        df = pd.DataFrame(columns=[
            "Date",
            "Allocation",
            "Action",
            "Portfolio_Value"
        ])

        last_asset = None
        last_value = INITIAL_CAPITAL


    # Detect action

    if last_asset == today_asset:

        action = "HOLD"

    else:

        action = "SWITCH"


    # Update portfolio value

    new_value = last_value

    if last_asset == "NIFTYBEES":

        daily_return = (nifty_today - nifty_yesterday) / nifty_yesterday
        new_value = last_value * (1 + daily_return)

    elif last_asset == "BANKBEES":

        daily_return = (bank_today - bank_yesterday) / bank_yesterday
        new_value = last_value * (1 + daily_return)

    # CASH remains unchanged


    new_entry = pd.DataFrame([{
        "Date": today,
        "Allocation": today_asset,
        "Action": action,
        "Portfolio_Value": round(new_value, 2)
    }])


    df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(LOG_FILE, index=False)


    message = f"""
📊 Portfolio Update

Date: {today}

Allocation: {today_asset}

Action: {action}

Portfolio Value: ₹{round(new_value, 2)}
"""


    print(message)

    send_message(message)


if __name__ == "__main__":

    update_portfolio()
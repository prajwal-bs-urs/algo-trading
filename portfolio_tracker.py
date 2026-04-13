from datetime import datetime
import os
import pandas as pd

from data_loader import get_data
from strategy import generate_signals
from telegram_alert import send_message


LOG_FILE = "portfolio_log.csv"

INITIAL_CAPITAL = 500000  # change later if needed


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


    if last_asset == today_asset:

        action = "HOLD"

    else:

        action = "SWITCH"


    new_entry = pd.DataFrame([{
        "Date": today,
        "Allocation": today_asset,
        "Action": action,
        "Portfolio_Value": last_value
    }])


    df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(LOG_FILE, index=False)


    message = f"""
📊 Portfolio Update

Date: {today}

Allocation: {today_asset}

Action: {action}

Portfolio Value: ₹{last_value}
"""


    print(message)

    send_message(message)


if __name__ == "__main__":

    update_portfolio()
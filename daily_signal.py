from data_loader import get_data
from strategy import generate_signals
from telegram_alert import send_message


SIGNAL_MAP = {
    0: "CASH",
    1: "NIFTYBEES",
    2: "BANKBEES"
}


def get_today_signal():

    print("Fetching latest signal...")

    data = get_data()

    data = generate_signals(data)

    today_signal = int(data.iloc[-1]["Signal"])
    yesterday_signal = int(data.iloc[-2]["Signal"])

    today_asset = SIGNAL_MAP[today_signal]
    yesterday_asset = SIGNAL_MAP[yesterday_signal]


    if today_signal == yesterday_signal:

        message = f"""
📊 Rotation Signal Update

Allocation unchanged → {today_asset}
"""

    else:

        message = f"""
📊 Rotation Signal Update

Previous → {yesterday_asset}
New → {today_asset}

Action → SWITCH
"""

    print(message)

    send_message(message)


if __name__ == "__main__":
    get_today_signal()
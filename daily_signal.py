from data_loader import get_data
from strategy import generate_signals
from telegram_alert import send_message
from portfolio_nav import compute_portfolio_nav

from datetime import datetime


INITIAL_CAPITAL = 100000


# ==============================
# ETF mapping
# ==============================

ETF_MAP = {
    1: "NIFTYBEES",
    2: "BANKBEES",
    3: "MIDCPNIFTY ETF",
    4: "GOLDBEES",
    5: "USDINR (Cash Proxy)"
}


SIGNAL_MAP = {
    1: "NIFTY",
    2: "BANK",
    3: "MIDCAP",
    4: "GOLD",
    5: "USDINR"
}


# ==============================
# Return computation
# ==============================

def compute_returns(data):

    allocator_nav, position = compute_portfolio_nav(data)

    allocator_return = (
        allocator_nav / INITIAL_CAPITAL - 1
    ) * 100

    nifty_return = (
        data["NIFTY"].iloc[-1]
        / data["NIFTY"].iloc[0]
        - 1
    ) * 100

    alpha = allocator_return - nifty_return

    return (
        allocator_nav,
        allocator_return,
        nifty_return,
        alpha,
        position,
    )


# ==============================
# Execution instruction block
# ==============================

def generate_execution_block(latest_signal, previous_signal):

    if latest_signal == previous_signal:

        return "NO TRADE REQUIRED ⏳ HOLD CURRENT POSITION"

    sell_etf = ETF_MAP[previous_signal]
    buy_etf = ETF_MAP[latest_signal]

    return f"""
🚨 ACTION REQUIRED

SELL: {sell_etf}
BUY: {buy_etf}
"""


# ==============================
# Telegram message builder
# ==============================

def generate_message():

    data = get_data()

    data = generate_signals(data)

    latest_signal = data["Signal"].iloc[-1]
    previous_signal = data["Signal"].iloc[-2]

    (
        allocator_nav,
        allocator_return,
        nifty_return,
        alpha,
        position,
    ) = compute_returns(data)

    latest_asset = SIGNAL_MAP[latest_signal]
    previous_asset = SIGNAL_MAP[previous_signal]
    etf = ETF_MAP[latest_signal]

    switch_required = (
        "YES ✅"
        if latest_signal != previous_signal
        else "NO ⏳ HOLD"
    )

    execution_block = generate_execution_block(
        latest_signal,
        previous_signal
    )

    timestamp = datetime.now().strftime("%d-%b-%Y %H:%M")

    message = f"""
📊 Tactical Allocator Dashboard

🕒 Time: {timestamp}

📍 Current Signal: {latest_asset}
📍 Previous Signal: {previous_asset}

🔄 Switch Required: {switch_required}

{execution_block}

🎯 Suggested ETF: {etf}

━━━━━━━━━━━━━━━━━━

💰 Portfolio NAV: ₹{allocator_nav:,.0f}

📈 Allocator Return: {allocator_return:.2f} %
📊 NIFTY Return: {nifty_return:.2f} %

⭐ Alpha vs NIFTY: {alpha:.2f} %

📦 Active Allocation: {ETF_MAP[position]}

━━━━━━━━━━━━━━━━━━

📅 Next Review: Friday after market close

Strategy: Macro Tactical Allocation v1
"""

    return message


# ==============================
# Script entry point
# ==============================

if __name__ == "__main__":

    msg = generate_message()

    print(msg)

    send_message(msg)
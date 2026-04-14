from daily_signal import get_latest_signal, SIGNAL_MAP, ETF_MAP

import pandas as pd
from datetime import datetime
import os


FILE_NAME = "signal_history.csv"


def log_signal():

    (
        latest_signal,
        previous_signal,
        allocator_return,
        nifty_return,
        alpha,
    ) = get_latest_signal()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    switch_required = latest_signal != previous_signal

    record = {

        "timestamp": now,
        "current_signal": SIGNAL_MAP[latest_signal],
        "previous_signal": SIGNAL_MAP[previous_signal],
        "switch_required": switch_required,
        "suggested_etf": ETF_MAP[latest_signal],
        "allocator_return_pct": round(allocator_return, 2),
        "nifty_return_pct": round(nifty_return, 2),
        "alpha_pct": round(alpha, 2),
    }

    df = pd.DataFrame([record])

    if os.path.exists(FILE_NAME):

        df.to_csv(FILE_NAME, mode="a", header=False, index=False)

    else:

        df.to_csv(FILE_NAME, index=False)


if __name__ == "__main__":

    log_signal()
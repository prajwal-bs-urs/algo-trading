from config import SHORT_WINDOW


def generate_signals(data):

    print("Generating enhanced relative strength signals...")

    data["RS"] = data["BANK"] / data["NIFTY"]

    data["RS_MA"] = data["RS"].rolling(SHORT_WINDOW).mean()

    data["NIFTY_MA"] = data["NIFTY"].rolling(SHORT_WINDOW).mean()
    data["BANK_MA"] = data["BANK"].rolling(SHORT_WINDOW).mean()

    data["Signal"] = 0

    data.loc[
        (data["RS"] > data["RS_MA"]) &
        (data["BANK"] > data["BANK_MA"]),
        "Signal"
    ] = 2

    data.loc[
        (data["RS"] < data["RS_MA"]) &
        (data["NIFTY"] > data["NIFTY_MA"]),
        "Signal"
    ] = 1

    return data
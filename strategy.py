MID_WINDOW = 126
LONG_WINDOW = 252

MIN_HOLD_DAYS = 10


def generate_signals(data):

    print("Generating macro tactical allocation signals (equity-priority mode)...")

    assets = ["NIFTY", "BANK", "MIDCAP", "GOLD", "USDINR"]

    # =============================
    # Dual momentum calculations
    # =============================

    for asset in assets:

        data[f"RET6_{asset}"] = data[asset].pct_change(MID_WINDOW)

        data[f"RET12_{asset}"] = data[asset].pct_change(LONG_WINDOW)

        data[f"SCORE_{asset}"] = (
            0.5 * data[f"RET6_{asset}"]
            + 0.5 * data[f"RET12_{asset}"]
        )

    # =============================
    # Allocation logic
    # =============================

    signals = []

    for i in range(len(data)):

        # Crash regime override

        if data["RET6_NIFTY"].iloc[i] < -0.10:

            signals.append(4)  # GOLD
            continue

        # =============================
        # Equity priority selection
        # =============================

        equity_scores = {

            1: data["SCORE_NIFTY"].iloc[i],
            2: data["SCORE_BANK"].iloc[i],
            3: data["SCORE_MIDCAP"].iloc[i]

        }

        valid_equities = {

            k: v for k, v in equity_scores.items()
            if v > 0
        }

        # If equities strong → choose best equity

        if len(valid_equities) > 0:

            best_equity = max(valid_equities, key=valid_equities.get)

            signals.append(best_equity)

            continue

        # =============================
        # Defensive asset selection
        # =============================

        gold_score = data["SCORE_GOLD"].iloc[i]

        usdinr_score = data["SCORE_USDINR"].iloc[i]

        if gold_score > usdinr_score:

            signals.append(4)

        else:

            signals.append(5)

    data["Signal"] = signals

    # =============================
    # Minimum holding filter
    # =============================

    filtered = []

    last_signal = 0

    holding_days = MIN_HOLD_DAYS

    for signal in data["Signal"]:

        if signal != last_signal:

            if holding_days >= MIN_HOLD_DAYS:

                last_signal = signal

                holding_days = 0

        filtered.append(last_signal)

        holding_days += 1

    data["Signal"] = filtered


    return data
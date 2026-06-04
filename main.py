from data_loader import get_data
from strategy import generate_signals

SIGNAL_LABELS = {
    0: "No position (warming up)",
    1: "NIFTY",
    2: "BANK",
    3: "MIDCAP",
    4: "GOLD",
    5: "USDINR",
}


def main():

    data = get_data()
    data = generate_signals(data)

    latest = data.iloc[-1]

    print("--- Latest Market Snapshot ---")
    print(f"NIFTY  : {latest['NIFTY']:.2f}  |  6M return: {latest['RET6_NIFTY']*100:.1f}%  |  Score: {latest['SCORE_NIFTY']:.4f}")
    print(f"BANK   : {latest['BANK']:.2f}  |  6M return: {latest['RET6_BANK']*100:.1f}%  |  Score: {latest['SCORE_BANK']:.4f}")
    print(f"MIDCAP : {latest['MIDCAP']:.2f}  |  6M return: {latest['RET6_MIDCAP']*100:.1f}%  |  Score: {latest['SCORE_MIDCAP']:.4f}")
    print(f"GOLD   : {latest['GOLD']:.2f}  |  6M return: {latest['RET6_GOLD']*100:.1f}%  |  Score: {latest['SCORE_GOLD']:.4f}")

    signal = int(latest["Signal"])
    label = SIGNAL_LABELS.get(signal, "Unknown")

    print(f"\nCurrent Signal : {signal} → Allocate to {label}")

    if signal in (1, 2, 3):
        print("Action: HOLD / BUY equity ETF")
    elif signal == 4:
        print("Action: HOLD / BUY GOLDBEES (crash regime)")
    elif signal == 5:
        print("Action: HOLD / BUY USDINR proxy (defensive)")
    else:
        print("Action: No position (strategy warming up)")


if __name__ == "__main__":
    main()

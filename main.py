from data_loader import get_data
from strategy import generate_signals


def main():

    data = get_data()
    data = generate_signals(data)

    latest = data.iloc[-1]

    print("Close:", latest["Close"])
    print("20DMA:", latest["Short_MA"])
    print("50DMA:", latest["Long_MA"])

    latest_signal = latest["Signal"]

    if latest_signal == 1:
        print("BUY signal generated")

    elif latest_signal == -1:
        print("SELL signal generated")

    else:
        print("No signal")


if __name__ == "__main__":
    main()
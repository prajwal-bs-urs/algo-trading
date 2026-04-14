INITIAL_CAPITAL = 100000
TRANSITION_COST = 0.002


def compute_portfolio_nav(data):

    capital = INITIAL_CAPITAL
    units = 0
    position = None

    for i in range(len(data)):

        signal = data["Signal"].iloc[i]

        price_map = {
            1: data["NIFTY"].iloc[i],
            2: data["BANK"].iloc[i],
            3: data["MIDCAP"].iloc[i],
            4: data["GOLD"].iloc[i],
            5: data["USDINR"].iloc[i],
        }

        if signal != position:

            if position is not None:

                exit_price = price_map[position]

                capital = units * exit_price

                # Apply transition cost
                capital *= (1 - TRANSITION_COST)

            entry_price = price_map[signal]

            units = capital / entry_price

            position = signal

    final_price = price_map[position]

    nav = units * final_price

    return nav, position
import pandas as pd
import numpy as np


TRADING_DAYS = 252


def calculate_cagr(equity_curve):

    equity = pd.Series(equity_curve)

    years = len(equity) / TRADING_DAYS

    return (equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1


def calculate_volatility(equity_curve):

    returns = pd.Series(equity_curve).pct_change().dropna()

    return returns.std() * np.sqrt(TRADING_DAYS)


def calculate_sharpe(equity_curve, risk_free_rate=0.05):

    returns = pd.Series(equity_curve).pct_change().dropna()

    excess_returns = returns - risk_free_rate / TRADING_DAYS

    return excess_returns.mean() / returns.std() * np.sqrt(TRADING_DAYS)


def calculate_sortino(equity_curve, risk_free_rate=0.05):

    returns = pd.Series(equity_curve).pct_change().dropna()

    downside = returns[returns < 0]

    return (
        (returns.mean() - risk_free_rate / TRADING_DAYS)
        / downside.std()
        * np.sqrt(TRADING_DAYS)
    )


def calculate_max_drawdown(equity_curve):

    equity = pd.Series(equity_curve)

    peak = equity.cummax()

    drawdown = (equity - peak) / peak

    return drawdown.min()


def calculate_calmar(cagr, max_drawdown):

    return cagr / abs(max_drawdown)


def calculate_win_rate(equity_curve):

    returns = pd.Series(equity_curve).pct_change().dropna()

    wins = (returns > 0).sum()

    return wins / len(returns)


def rolling_cagr(equity_curve, window=756):

    equity = pd.Series(equity_curve)

    result = []

    for i in range(window, len(equity)):

        start = equity.iloc[i - window]

        end = equity.iloc[i]

        years = window / TRADING_DAYS

        result.append((end / start) ** (1 / years) - 1)

    return pd.Series(result)


def rolling_drawdown(equity_curve):

    equity = pd.Series(equity_curve)

    peak = equity.cummax()

    drawdown = (equity - peak) / peak

    return drawdown


def generate_performance_report(equity_curve):

    cagr = calculate_cagr(equity_curve)

    vol = calculate_volatility(equity_curve)

    sharpe = calculate_sharpe(equity_curve)

    sortino = calculate_sortino(equity_curve)

    max_dd = calculate_max_drawdown(equity_curve)

    calmar = calculate_calmar(cagr, max_dd)

    win_rate = calculate_win_rate(equity_curve)

    print("\n========== PERFORMANCE METRICS ==========")

    print("CAGR:", round(cagr * 100, 2), "%")

    print("Volatility:", round(vol * 100, 2), "%")

    print("Sharpe Ratio:", round(sharpe, 2))

    print("Sortino Ratio:", round(sortino, 2))

    print("Max Drawdown:", round(max_dd * 100, 2), "%")

    print("Calmar Ratio:", round(calmar, 2))

    print("Win Rate:", round(win_rate * 100, 2), "%")

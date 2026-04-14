import pandas as pd
import numpy as np


TRADING_DAYS = 252


def calculate_beta(strategy_returns, benchmark_returns):

    covariance = np.cov(strategy_returns, benchmark_returns)[0][1]

    variance = np.var(benchmark_returns)

    return covariance / variance


def calculate_alpha(strategy_returns, benchmark_returns):

    beta = calculate_beta(strategy_returns, benchmark_returns)

    strategy_mean = np.mean(strategy_returns) * TRADING_DAYS

    benchmark_mean = np.mean(benchmark_returns) * TRADING_DAYS

    return strategy_mean - beta * benchmark_mean


def information_ratio(strategy_returns, benchmark_returns):

    excess = strategy_returns - benchmark_returns

    return np.mean(excess) / np.std(excess) * np.sqrt(TRADING_DAYS)


def up_capture(strategy_returns, benchmark_returns):

    up_mask = benchmark_returns > 0

    return (
        strategy_returns[up_mask].mean()
        / benchmark_returns[up_mask].mean()
    )


def down_capture(strategy_returns, benchmark_returns):

    down_mask = benchmark_returns < 0

    return (
        strategy_returns[down_mask].mean()
        / benchmark_returns[down_mask].mean()
    )


def benchmark_report(equity_curve, benchmark_prices):

    strategy_returns = pd.Series(equity_curve).pct_change().dropna().values

    benchmark_returns = (
        benchmark_prices
        .pct_change()
        .dropna()
        .values
    )

    # Align lengths safely

    min_len = min(len(strategy_returns), len(benchmark_returns))

    strategy_returns = strategy_returns[-min_len:]

    benchmark_returns = benchmark_returns[-min_len:]

    beta = calculate_beta(strategy_returns, benchmark_returns)

    alpha = calculate_alpha(strategy_returns, benchmark_returns)

    info_ratio = information_ratio(strategy_returns, benchmark_returns)

    up_cap = up_capture(strategy_returns, benchmark_returns)

    down_cap = down_capture(strategy_returns, benchmark_returns)

    print("\n========== BENCHMARK COMPARISON ==========")

    print("Beta vs NIFTY:", round(beta, 2))

    print("Alpha (annualized):", round(alpha * 100, 2), "%")

    print("Information Ratio:", round(info_ratio, 2))

    print("Up Capture Ratio:", round(up_cap, 2))

    print("Down Capture Ratio:", round(down_cap, 2))
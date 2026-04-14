from datetime import datetime
import pandas as pd

from telegram_alert import send_message


LOG_FILE = "portfolio_log.csv"


def generate_monthly_report():

    df = pd.read_csv(LOG_FILE)

    df["Date"] = pd.to_datetime(df["Date"])


    today = datetime.today()

    if today.month == 1:

        report_month = 12
        report_year = today.year - 1

    else:

        report_month = today.month - 1
        report_year = today.year


    monthly_data = df[

        (df["Date"].dt.month == report_month) &
        (df["Date"].dt.year == report_year)

    ]


    if len(monthly_data) < 2:

        print("Not enough data for monthly report.")
        return


    start_value = monthly_data.iloc[0]["Portfolio_Value"]
    end_value = monthly_data.iloc[-1]["Portfolio_Value"]

    benchmark_start = monthly_data.iloc[0]["Benchmark_Value"]
    benchmark_end = monthly_data.iloc[-1]["Benchmark_Value"]


    strategy_return = ((end_value / start_value) - 1) * 100

    benchmark_return = ((benchmark_end / benchmark_start) - 1) * 100

    alpha = strategy_return - benchmark_return


    allocation = monthly_data.iloc[-1]["Allocation"]


    month_name = datetime(report_year, report_month, 1).strftime("%B %Y")


    message = f"""
📊 Monthly Strategy Report

Month: {month_name}

Strategy Return: {round(strategy_return,2)}%

Benchmark Return: {round(benchmark_return,2)}%

Outperformance: {round(alpha,2)}%

Current Allocation: {allocation}

Portfolio Value: ₹{round(end_value,2)}
"""


    print(message)

    send_message(message)


if __name__ == "__main__":

    generate_monthly_report()
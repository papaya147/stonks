import yfinance as yf
from datetime import datetime, timedelta, timezone
import os
import pandas as pd


def save_stock_data() -> None:
    with open("../../stock list.txt", "r") as file:
        data = file.read()
    stock_list = list(set(data.split()))

    stock_tickers = yf.Tickers(" ".join(stock_list))

    for stock in stock_list:
        stock_ticker = stock_tickers.tickers[stock]

        end_date = datetime.now()
        end_date = end_date.replace(tzinfo=timezone.utc)
        start_date = end_date - timedelta(days=7)
        exists = False

        # check if the csv exists already, if it does, make start_date from the latest date
        try:
            file_name = f"../../data/stock-prices/{stock}.csv"
            data = pd.read_csv(file_name)
            latest_date_record = data["Datetime"][len(data) - 1]
            next_date = (datetime.strptime(latest_date_record,
                                           "%Y-%m-%d %H:%M:%S%z") + timedelta(days=1))
            next_date = next_date.replace(tzinfo=timezone.utc)
            if next_date > start_date:
                start_date = next_date
            exists = True
        except Exception as e:
            pass

        hist = stock_ticker.history(
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            period="max", interval="1m",
        )
        hist.to_csv(f"../../data/stock-prices/{stock}.csv",
                    mode="a" if exists else "w", header=not exists)


save_stock_data()

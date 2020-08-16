from datetime import timedelta, date
from pathlib import Path
import requests
import ast
import os
import csv
import time

"""
r=days ago
zig=

https://bitcoincharts.com/charts/chart.json?m=krakenUSD&SubmitButton=Draw&r=5&i=15-min&c=1&s=2020-07-29&e=2020-07-31&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&

url = r'https://bitcoincharts.com/charts/chart.json?m=bitstampUSD&SubmitButton=Draw&r=10&i=30-min&c=0&s=&e=&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&'
url2 = r'https://bitcoincharts.com/charts/chart.json?m=krakenUSD&SubmitButton=Draw&r=5&i=15-min&c=1&s=2020-07-30&e=2020-07-30&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&'
"""


def dates(start, end):
    for n in range(int((end - start).days)):
        yield start + timedelta(n)


def get_btc(path, date1, date2, period="5-min", delay=3):

    """

    period = '5-min', 'Hourly'

    """

    url2_1 = (
        r"https://bitcoincharts.com/charts/chart.json?m=krakenUSD&SubmitButton=Draw&r=5&i="
        + period
        + "&c=1&s="
    )
    url2_2 = r"&Prev=&Next=&t=S&b=&a1=&m1=10&a2=&m2=25&x=0&i1=&i2=&i3=&i4=&v=1&cv=0&ps=0&l=0&p=0&"

    Path(path).mkdir(parents=True, exist_ok=True)

    for d in dates(date1, date2):

        date = d.strftime("%Y-%m-%d")

        r = requests.get(url2_1 + date + "&e=" + date + url2_2)
        assert r.status_code == 200, "Page returned invalid response"

        data = ast.literal_eval(r.text)
        assert len(data[0]) == 8, "Data was improperly parsed"

        headers = [
            "Timestamp",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume(BTC)",
            "Volume(Currency)",
            "WeightedPrice",
        ]

        with open(os.path.join(path, f"{date}.csv"), mode="w", newline="") as data_file:
            writer = csv.writer(data_file)
            writer.writerow(headers)
            writer.writerows(data)

        time.sleep(delay)

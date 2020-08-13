from collections import namedtuple
from finta import TA
from .params import *
import pandas as pd


def preprocess(X: pd.DataFrame, validation=False):

    if validation and list(X.columns) != HEADERS:
        raise NameError("Headers do not match!")

    data = pd.DataFrame()
    data["Change"] = X["Close"].diff(periods=PREDICTION_WINDOW_PERIOD)

    periods = [10, 50, 100, 200]
    for period in periods:
        data[period] = getattr(TA, "SMA")(X, period=period)

    macd = TA.MACD(X)
    data["MACD"] = macd["MACD"]
    data["SIGNAL"] = macd["SIGNAL"]
    data["DIFF"] = macd["MACD"] - macd["SIGNAL"]

    data["RSI"] = TA.RSI(X, period=14)
    data["MOM"] = TA.MOM(X)

    data["VOL"] = X["Volume(BTC)"]

    data["Change%"] = (
        data["Change"] / X["Close"]
    )  # get percent change // has to be above dropna

    data = data.dropna()
    y1 = data["Change"]
    y1[y1 > 0] = 1
    y1[y1 < 0] = 0

    y2 = data["Change%"]

    y = namedtuple("y", "classifier regressor")  # using named tuple for immutability

    return (data.drop(["Change", "Change%"], axis=1), y(classifier=y1, regressor=y2))

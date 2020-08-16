from collections import namedtuple
import numpy as np
import pandas as pd


def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


class Simulator:

    history = pd.DataFrame(
        columns=[
            "Price",
            "Action",
            "Trade",
            "Cash($)",
            "Holding(BTC)",
            "Capital($)",
            "Capped",
        ]
    )

    def __init__(self, data, predictor, **kwargs):

        self.data = data
        self.predictor = predictor
        self.bitcoin = kwargs.get("bitcoin", 1)
        self.cash = kwargs.get("cash", 200)
        self.fee = kwargs.get("fee", 0)
        self.relative = kwargs.get(
            "relative", True
        )  # bitcoin trades are % of total rather than numerical amount

    def play(self, verbose=1):

        bitcoin_ = self.bitcoin
        cash_ = self.cash

        assets = namedtuple("assets", "bitcoin cash")

        data_length = len(self.data)  # for speed

        for time, d in enumerate(np.array(self.data)):

            info = {}

            prediction = self.predictor.predict(
                d, time, assets(bitcoin=bitcoin_, cash=cash_)
            )

            actions = {
                -1: lambda amount: min(amount, bitcoin_),
                0: lambda amount: 0,
                1: lambda amount: min(amount, cash_ / d[0]),
            }

            traded_btc = actions[prediction[0]](prediction[1])

            info.update({"Capped": prediction[1] - traded_btc})

            bitcoin_ += traded_btc * prediction[0]
            cash_ += traded_btc * prediction[0] * -1 * d[0]

            if prediction[0] is -1:
                cash_ -= traded_btc * self.fee * d[0]
            elif prediction[0] is 1:
                bitcoin_ -= traded_btc * self.fee

            info.update(
                {
                    "Price": d[0],
                    "Action": prediction[0],
                    "Trade": prediction[1],
                    "Cash($)": cash_,
                    "Holding(BTC)": bitcoin_,
                    "Capital($)": (cash_ + d[0] * bitcoin_),
                }
            )

            self.history = self.history.append(info, ignore_index=True)

            printProgressBar(
                time + 1, data_length, prefix="progress:", suffix="complete"
            )

        return self.history

    def multi_play(self, n=5):

        histories = []
        for i in range(5):

            histories.append(self.play())

        self.histories = histories

        return histories


class Predictor:
    def __init__(self, **kwargs):
        self.preceding = kwargs.get("preceding", 0)
        self.history = []
        self.time = kwargs.get("time", 0)

    def get_past(self):

        if len(self.history) >= self.preceding:

            return self.history[-self.preceding :]

        else:
            return False

    def predict(self, data, time, assets):

        self.history.append(data)
        raw_data = self.get_past()

        if raw_data:
            return self.predict_engine(raw_data, time, assets)

        else:
            return (0, 0)

    def predict_engine(self, data, time, assets):

        """
        OVERRIDE THIS METHOD

        arg1:

        sell: -1
        hold: 0
        buy: 1

        arg2:

        percent traded

        """

        return (1, 0.25)

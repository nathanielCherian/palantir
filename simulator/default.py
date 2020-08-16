from .sim import Simulator, Predictor
from palantir.predictors import predict
from palantir.params import HEADERS
import numpy as np
import pandas as pd


class BacktestPredictor(Predictor):
    def __init__(self, clfs, **kwargs):
        super().__init__(**kwargs)
        self.clfs = clfs

    def predict_engine(self, data, time, assets):

        complete_data = pd.DataFrame(data, columns=HEADERS[1:])

        prediction = predict(complete_data, self.clfs)

        n = np.argmax(prediction[0])

        if n == 0:
            return (-1, prediction[0][n] * assets.bitcoin)
        else:
            return (1, prediction[0][n] * assets.cash)

        return (randint(-1, 1), 1)

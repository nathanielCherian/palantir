from .params import *
import numpy as np

"""
Holds trading strategies and optimizers
"""


def simple_agg(predictions):

    if predictions[0] < 1:
        return -1
    else:
        return 1


def smart_agg(predictions, cap):

    if abs(predictions[1]) > cap:

        if predictions[0] == 1:

            return 1
        else:

            return -1

    return 0


def agg(predictions, assets):
    n = np.argmax(prediction[0])

    if n == 0:
        return (-1, prediction[0][n] * assets.bitcoin)
    else:
        return (1, prediction[0][n] * assets.cash)

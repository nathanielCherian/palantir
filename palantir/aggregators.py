from .params import *

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

from .params import *

def simple_agg(predictions):

    if predictions[0] < 1:
        return -1
    else:
        return 1
from .params import *
import pandas as pd
import numpy as np
import os


def load_data(directory, test_size=None):
    data = pd.DataFrame(columns=HEADERS)

    for filename in os.listdir(directory):
        data = pd.concat(
            [data, pd.read_csv(os.path.join(directory, filename), index_col=False)]
        )

    if test_size:
        cut = int(len(data) * test_size)
        return (data[:-cut].reset_index(drop=True), data[-cut:].reset_index(drop=True))

    return data

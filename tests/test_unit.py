import pytest
import os
import pandas as pd
import palantir

def rootdir():
    return os.path.dirname(os.path.abspath(__file__))

headers = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume(BTC)', 'Volume(Currency)', 'WeightedPrice']
data = pd.DataFrame(columns=headers)
for filename in os.listdir(os.path.join(rootdir(), 'data')):
    data = pd.concat([data, pd.read_csv(os.path.join(rootdir(), 'data', filename), index_col=False)])



def test_preprocess():

    X, y = palantir.preprocess(data)

    assert isinstance(X, pd.DataFrame)
    assert sum(list(X.iloc[-1])) == 33610.54036843656
    assert y.classifier.iloc[-1] == 0.0
    assert y.regressor.iloc[-1] == -0.014002065878572249






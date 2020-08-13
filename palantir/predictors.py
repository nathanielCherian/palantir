from pathlib import Path
from . import preprocess
from sklearn.model_selection import train_test_split
from .params import *
import pandas as pd
import joblib
import os

def create_models(rawdata: pd.DataFrame, evaluate=True, verbose=0):

    Path(MODELS_PATH).mkdir(parents=True, exist_ok=True)

    X, y_collection = preprocess(rawdata)

    for model in MODELS:
        clf = model['model'](**model['params'])

        y = getattr(y_collection, model['type'])
        clf = clf.fit(X, y)

        joblib.dump(clf, os.path.join(MODELS_PATH, f'{model["name"]}.pkl'))

        if verbose > 0:
            print(model['name'] + ': ', clf.score(X, y))



def predict(rawdata: pd.DataFrame, clfs=None):

    if len(rawdata) < MINIMUM_DATA:
        raise Exception(f"Minimum data requirement of {MINIMUM_DATA} not met!")

    
    X = preprocess(rawdata)[0]


    if not clfs:
        clfs = []
        for name in [model['name']+'.pkl' for model in MODELS]:
            clfs.append(joblib.load(os.path.join(MODELS_PATH, name)))


    predictions = []
    for clf in clfs:
        predictions.append(getattr(clf, 'predict')(X[-1:])[0])

    return predictions







from sklearn.model_selection import train_test_split
from pathlib import Path
from . import preprocess
from .params import *
import pandas as pd
import joblib
import os


def create_models(rawdata: pd.DataFrame, evaluate=True, verbose=0):

    Path(MODELS_PATH).mkdir(parents=True, exist_ok=True)

    X, y_collection = preprocess(rawdata)

    clfs = []
    for model in MODELS:
        clf = model["model"](**model["params"])

        y = getattr(y_collection, model["type"])
        clf = clf.fit(X, y)

        joblib.dump(clf, os.path.join(MODELS_PATH, f'{model["name"]}.pkl'))

        clfs.append((clf, model['predictor']))

        if verbose > 0:
            print(model["name"] + ": ", clf.score(X, y))

    return clfs


def load_models(clf_names=[(model["name"] + ".pkl", model['predictor']) for model in MODELS]):
    clfs = []
    for (name, predictor) in clf_names:
        clfs.append((joblib.load(os.path.join(MODELS_PATH, name)), predictor))

    return clfs


def predict(rawdata: pd.DataFrame, clfs=None):

    if len(rawdata) < MINIMUM_DATA:
        raise Exception(f"Minimum data requirement of {MINIMUM_DATA} not met!")

    X = preprocess(rawdata)[0]

    if not clfs:
        raise NotImplementedError


    predictions = []
    for (clf, predictor) in clfs:
        predictions.append(getattr(clf, predictor)(X[-1:])[0])

    return predictions

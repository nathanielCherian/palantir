from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression

"""
Parameters for the Palantir Project

"""

MODELS_PATH = "models"

MODELS = [
    {
        "name": "rfclf",
        "model": RandomForestClassifier,
        "type": "classifier",
        "predictor": "predict_proba",
        "params": {"n_estimators": 100},
    },
    {
        "name": "linreg",
        "model": LinearRegression,
        "type": "regressor",
        "predictor": "predict",
        "params": {},
    },
]


MINIMUM_DATA = 200

HEADERS = [
    "Timestamp",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume(BTC)",
    "Volume(Currency)",
    "WeightedPrice",
]

PREDICTION_WINDOW_PERIOD = 10


TRADING_FEE = 0.0026
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression

"""
Parameters for the Palantir Project

"""

MODELS_PATH = 'models'

MODELS = [
    {
        'name':'rfclf',
        'model':RandomForestClassifier,
        'type':'classifier',
        'predictior':'predict_proba',
        'params':{
            'n_estimators':100
        }
    },

    {
        'name':'linreg',
        'model':LinearRegression,
        'type':'regressor',
        'predictior':'predict',
        'params':{
        }
    }
]

MINIMUM_DATA = 200

HEADERS = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume(BTC)', 'Volume(Currency)', 'WeightedPrice']

PREDICTION_WINDOW_PERIOD = 12
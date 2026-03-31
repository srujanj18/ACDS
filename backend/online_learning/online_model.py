from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import SGDClassifier


MODELS_DIR = Path(__file__).resolve().parents[2] / "models"
ONLINE_MODEL_PATH = MODELS_DIR / "online_model.pkl"


class OnlineModel:
    def __init__(self):
        self.model = SGDClassifier(loss="log_loss", learning_rate="optimal")
        self.initialized = False

    def initial_train(self, X, y):
        self.model.partial_fit(X, y, classes=np.unique(y))
        self.initialized = True
        print("Online model initialized")

    def predict(self, X):
        if not self.initialized:
            raise Exception("Model not initialized")

        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def update(self, X, y):
        if not self.initialized:
            self.initial_train(X, y)
        else:
            self.model.partial_fit(X, y)

        print("Online model updated")

    def save(self):
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, ONLINE_MODEL_PATH)
        print("Online model saved")

    def load(self):
        self.model = joblib.load(ONLINE_MODEL_PATH)
        self.initialized = True
        print("Online model loaded")

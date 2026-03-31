from pathlib import Path

import joblib
import numpy as np

from .online_model import OnlineModel


MODELS_DIR = Path(__file__).resolve().parents[2] / "models"


class OnlineUpdater:
    def __init__(self):
        print("Initializing Online Updater...")

        # Resolve model files from the repository root, not the shell cwd.
        self.detection_model = joblib.load(MODELS_DIR / "detection_model.pkl")
        self.scaler = joblib.load(MODELS_DIR / "scaler.pkl")
        self.encoder = joblib.load(MODELS_DIR / "encoder.pkl")

        self.online_model = OnlineModel()

        try:
            self.online_model.load()
        except Exception:
            print("No online model found. Will initialize.")

    def preprocess(self, X):
        X = np.array(X)
        return self.scaler.transform(X)

    def detect(self, X):
        X_scaled = self.preprocess(X)
        prediction = self.detection_model.predict(X_scaled)
        label = self.encoder.inverse_transform(prediction)
        return prediction, label

    def update_model(self, X):
        X_scaled = self.preprocess(X)
        y_pred = self.detection_model.predict(X_scaled)
        self.online_model.update(X_scaled, y_pred)
        self.online_model.save()

    def smart_update(self, X, confidence_threshold=0.9):
        X_scaled = self.preprocess(X)
        probs = self.detection_model.predict_proba(X_scaled)
        confidence = np.max(probs)

        if confidence >= confidence_threshold:
            y_pred = self.detection_model.predict(X_scaled)
            self.online_model.update(X_scaled, y_pred)
            self.online_model.save()
            print(f"Updated (confidence={confidence:.2f})")
        else:
            print(f"Skipped update (low confidence={confidence:.2f})")

    def process(self, X):
        _, label = self.detect(X)
        print(f"Detected: {label[0]}")
        self.smart_update(X)
        return label[0]

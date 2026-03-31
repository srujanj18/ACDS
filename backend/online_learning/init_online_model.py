import joblib
import numpy as np
from online_model import OnlineModel


def initialize():
    print("🚀 Initializing online model...")

    scaler = joblib.load("../../models/scaler.pkl")

    n_features = len(scaler.mean_)

    # Dummy data just to initialize model
    X = np.random.rand(100, n_features)
    y = np.random.randint(0, 2, 100)

    model = OnlineModel()
    model.initial_train(X, y)
    model.save()


if __name__ == "__main__":
    initialize()
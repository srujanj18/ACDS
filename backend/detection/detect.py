import joblib
import numpy as np
from utils.preprocessing import Preprocessor
from utils.logger import get_logger

logger = get_logger(__name__)

class Detector:
    def __init__(self):
        self.model = joblib.load('../../models/detection_model.pkl')
        self.preprocessor = Preprocessor()
    
    def predict(self, flow):
        features = self.preprocessor.preprocess_flow(flow)
        features = np.array(features).reshape(1, -1)
        anomaly_score = self.model.decision_function(features)[0]
        prediction = self.model.predict(features)[0]
        return -anomaly_score if prediction == -1 else 0.0  # Higher score = more anomalous



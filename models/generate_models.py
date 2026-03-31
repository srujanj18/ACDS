import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd
import numpy as np

# Load sample data
df = pd.read_csv('../data/sample_traffic.csv')
features = ['bytes_sent', 'bytes_received', 'duration', 'packet_count']
X = df[features].values

# Train detection model
scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)
model = IsolationForest(contamination=0.2).fit(X_scaled)

# Save
joblib.dump(model, 'detection_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
encoder = LabelEncoder().fit(df['protocol'])
joblib.dump(encoder, 'encoder.pkl')

print("Models generated!")


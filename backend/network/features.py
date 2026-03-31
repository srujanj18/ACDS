import numpy as np
import pandas as pd


def compute_features(flow):

    lengths = flow["packet_lengths"]
    times = flow["timestamps"]

    duration = max(times) - min(times) if len(times) > 1 else 0

    features = {
        "Flow Duration": duration,
        "Total Fwd Packets": flow["packet_count"],
        "Flow Bytes/s": flow["byte_count"] / duration if duration > 0 else 0,

        "Packet Length Mean": np.mean(lengths),
        "Packet Length Std": np.std(lengths),
        "Packet Length Max": np.max(lengths),
        "Packet Length Min": np.min(lengths),

        "Flow Packets/s": flow["packet_count"] / duration if duration > 0 else 0,
    }

    return features


def to_dataframe(features):
    df = pd.DataFrame([features])
    df = df.fillna(0)
    return df
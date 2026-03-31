import pandas as pd


FEATURE_ALIASES = {
    "Packet Length Max": "Max Packet Length",
    "Packet Length Min": "Min Packet Length",
}


def preprocess_features(features_dict, scaler):
    df = pd.DataFrame([features_dict]).rename(columns=FEATURE_ALIASES)
    df = df.fillna(0)
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    expected_columns = getattr(scaler, "feature_names_in_", None)
    if expected_columns is not None:
        df = df.reindex(columns=expected_columns, fill_value=0)

    try:
        X = scaler.transform(df)
    except Exception as e:
        print(f"Scaling error: {e}")
        return None

    return X

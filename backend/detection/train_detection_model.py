import pandas as pd
import numpy as np
import glob
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight

from xgboost import XGBClassifier


# =========================
# LOAD DATA
# =========================
def load_data(sample_frac=0.3):
    files = glob.glob("../../data/*.csv")

    if len(files) == 0:
        raise Exception("❌ No CSV files found")

    print(f"📂 Found {len(files)} files")

    df_list = []

    for file in files:
        print(f"Loading: {file}")

        temp_df = pd.read_csv(file)
        temp_df.columns = temp_df.columns.str.strip()

        # Reduce memory usage
        temp_df = temp_df.sample(frac=sample_frac, random_state=42)

        df_list.append(temp_df)

    df = pd.concat(df_list, ignore_index=True)

    print("✅ Combined dataset:", df.shape)

    return df


# =========================
# PREPROCESS
# =========================
def preprocess(df):
    print("🔧 Preprocessing...")

    # Clean columns
    df.columns = df.columns.str.strip()

    # Remove invalid values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    print("Before filtering:", df.shape)

    # =========================
    # REMOVE RARE CLASSES (FIXED)
    # =========================
    counts = df["Label"].value_counts()

    print("\n📊 Class distribution BEFORE filtering:\n")
    print(counts.head(20))

    # Keep only classes with enough samples
    valid_classes = counts[counts > 100].index   # 👈 increase threshold

    df = df[df["Label"].isin(valid_classes)]

    print("\nAfter filtering rare classes:", df.shape)

    counts_after = df["Label"].value_counts()
    print("\n📊 Class distribution AFTER filtering:\n")
    print(counts_after.head(20))

    # =========================
    # ENCODE LABELS
    # =========================
    encoder = LabelEncoder()
    df["Label"] = encoder.fit_transform(df["Label"])

    y = df["Label"]

    # =========================
    # DROP NON-NUMERIC
    # =========================
    X = df.drop("Label", axis=1)

    drop_cols = ["Flow ID", "Source IP", "Destination IP", "Timestamp"]
    X = X.drop([c for c in drop_cols if c in X.columns], axis=1)

    # Convert to numeric
    X = X.apply(pd.to_numeric, errors='coerce')
    X = X.fillna(0)

    print("✅ Features shape:", X.shape)

    # =========================
    # SCALE
    # =========================
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, encoder


# =========================
# TRAIN MODEL
# =========================
def train():
    df = load_data(sample_frac=0.3)

    X, y, scaler, encoder = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # =========================
    # HANDLE CLASS IMBALANCE
    # =========================
    classes = np.unique(y_train)

    weights = compute_class_weight(
        class_weight='balanced',
        classes=classes,
        y=y_train
    )

    class_weights = dict(zip(classes, weights))

    sample_weights = np.array([class_weights[y] for y in y_train])

    print("⚖️ Class weights applied")

    # =========================
    # MODEL (CPU optimized)
    # =========================
    model = XGBClassifier(
        n_estimators=150,
        max_depth=8,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        tree_method="hist",   # avoids GPU warning
        n_jobs=-1
    )

    print("🚀 Training model...")

    model.fit(X_train, y_train, sample_weight=sample_weights)

    # =========================
    # EVALUATION
    # =========================
    pred = model.predict(X_test)

    print("\n📊 Model Performance:\n")
    print(classification_report(y_test, pred, zero_division=0))

    # =========================
    # SAVE MODELS
    # =========================
    os.makedirs("../../models", exist_ok=True)

    joblib.dump(model, "../../models/detection_model.pkl")
    joblib.dump(scaler, "../../models/scaler.pkl")
    joblib.dump(encoder, "../../models/encoder.pkl")

    print("💾 Detection model saved successfully!")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("🔥 Training Detection Model (Improved Version)")
    train()
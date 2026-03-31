from pathlib import Path

import joblib
from scapy.all import sniff

from features import compute_features, to_dataframe
from flow_extractor import get_completed_flows, update_flow


MODELS_DIR = Path(__file__).resolve().parents[2] / "models"

model = joblib.load(MODELS_DIR / "detection_model.pkl")
scaler = joblib.load(MODELS_DIR / "scaler.pkl")
encoder = joblib.load(MODELS_DIR / "encoder.pkl")


def process_packet(packet):
    key = update_flow(packet)

    if key is None:
        return

    completed_flows = get_completed_flows(timeout=5)

    for key, flow in completed_flows:
        features = compute_features(flow)
        df = to_dataframe(features)

        try:
            X = scaler.transform(df)
        except Exception:
            continue

        pred = model.predict(X)
        label = encoder.inverse_transform(pred)
        src_ip = key[0]

        print(f"{src_ip} -> {label[0]}")


def start_sniffing():
    print("Starting packet capture...")

    try:
        sniff(prn=process_packet, store=0)
    except RuntimeError as e:
        if "winpcap is not installed" in str(e).lower():
            print(
                "Packet capture unavailable on Windows. Install Npcap with "
                "WinPcap-compatible mode enabled, then rerun."
            )
            return False
        raise

    return True


if __name__ == "__main__":
    start_sniffing()

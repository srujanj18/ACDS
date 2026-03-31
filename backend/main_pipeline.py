from pathlib import Path

import joblib
from scapy.all import sniff

from defense.firewall import block_ip
from network.features import compute_features
from network.flow_extractor import get_completed_flows, update_flow
from online_learning.update import OnlineUpdater
from utils.logger import log_event
from utils.preprocessing import preprocess_features


MODELS_DIR = Path(__file__).resolve().parents[1] / "models"

detection_model = joblib.load(MODELS_DIR / "detection_model.pkl")
scaler = joblib.load(MODELS_DIR / "scaler.pkl")
encoder = joblib.load(MODELS_DIR / "encoder.pkl")

online_updater = OnlineUpdater()


def process_packet(packet):
    key = update_flow(packet)

    if key is None:
        return

    completed_flows = get_completed_flows(timeout=5)

    for key, flow in completed_flows:
        try:
            features = compute_features(flow)
            X = preprocess_features(features, scaler)

            if X is None:
                continue

            pred = detection_model.predict(X)
            label = encoder.inverse_transform(pred)[0]
            src_ip = key[0]

            log_event(f"Detected: {src_ip} -> {label}")

            if label != "BENIGN":
                log_event(f"Attack detected: {label} from {src_ip}")
                block_ip(src_ip)
                online_updater.smart_update(X)

        except Exception as e:
            log_event(f"Error: {e}")


def start_system():
    log_event("ACDS system starting packet capture")

    try:
        sniff(prn=process_packet, store=0)
    except RuntimeError as e:
        if "winpcap is not installed" in str(e).lower():
            log_event(
                "Packet capture unavailable on Windows. Install Npcap with "
                "WinPcap-compatible mode enabled, then rerun the backend."
            )
            return False
        raise

    return True


if __name__ == "__main__":
    start_system()

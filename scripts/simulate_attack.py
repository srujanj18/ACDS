from pathlib import Path
import random
import sys
import time


LOGS_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_FILE = LOGS_DIR / "acds.log"

LOGS_DIR.mkdir(parents=True, exist_ok=True)

attacks = ["DDoS", "PortScan", "Bot", "DoS Hulk"]


def safe_print(message):
    try:
        print(message)
    except UnicodeEncodeError:
        fallback = message.encode(
            sys.stdout.encoding or "utf-8", errors="replace"
        ).decode(sys.stdout.encoding or "utf-8", errors="replace")
        print(fallback)


def append_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def generate_ip():
    return f"192.168.1.{random.randint(1, 255)}"


safe_print("Simulating attacks...")

while True:
    ip = generate_ip()
    attack = random.choice(attacks)

    log_line = f"[SIMULATION] Detected: {ip} -> {attack}"
    append_log(log_line)

    if random.random() > 0.5:
        append_log(f"[SIMULATION] Blocking IP: {ip}")

    safe_print(log_line)
    time.sleep(2)

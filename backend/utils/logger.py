from datetime import datetime
from pathlib import Path
import sys


LOGS_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_FILE = LOGS_DIR / "acds.log"


def log_event(message):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"

    try:
        print(log_message)
    except UnicodeEncodeError:
        safe_message = log_message.encode(
            sys.stdout.encoding or "utf-8", errors="replace"
        ).decode(sys.stdout.encoding or "utf-8", errors="replace")
        print(safe_message)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

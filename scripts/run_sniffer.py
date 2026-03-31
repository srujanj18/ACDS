import os
import subprocess
import sys


print("Starting Packet Sniffer...")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
script_path = os.path.join(base_dir, "backend", "network", "sniffer.py")

subprocess.run([sys.executable, script_path], check=False)

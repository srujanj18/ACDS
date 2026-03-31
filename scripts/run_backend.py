import os
import subprocess

print("🚀 Starting ACDS Backend...")

# Get current project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build correct path
script_path = os.path.join(BASE_DIR, "backend", "main_pipeline.py")

# Run using venv python
venv_python = os.path.join(BASE_DIR, "acds_env", "Scripts", "python.exe")
subprocess.run([venv_python, script_path])

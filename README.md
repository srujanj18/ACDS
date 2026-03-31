# ACDS

<div align="center">

## AI Cyber Defense System

### Autonomous detection. Adaptive learning. Live cyber operations visibility.

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-0b1320?style=for-the-badge&logo=python&logoColor=7dd3fc">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-Dashboard-07111b?style=for-the-badge&logo=streamlit&logoColor=ff6b6b">
  <img alt="XGBoost" src="https://img.shields.io/badge/XGBoost-Detection-08141a?style=for-the-badge&logoColor=9ae6b4">
  <img alt="Scikit Learn" src="https://img.shields.io/badge/Scikit--Learn-Online%20Learning-0d1b2a?style=for-the-badge&logo=scikitlearn&logoColor=fbbf24">
</p>

```text
[ INGRESS ] ---> [ FLOW ENGINE ] ---> [ FEATURE GRID ] ---> [ AI DETECTION ] ---> [ RESPONSE ]
       \___________________________________________________________________________________/
                                         |
                                         v
                              [ LIVE COMMAND CENTER ]
```

</div>

---

## System Vision

ACDS is a futuristic cyber defense platform built to monitor live traffic, extract flow intelligence, score behavior through machine learning, adapt through online updates, and surface everything inside a command-center style dashboard.

The project is designed to feel like a compact SOC pipeline:

- capture traffic
- convert packets into features
- classify suspicious behavior
- react to threats
- display live telemetry for analysts and demos

---

## Why ACDS

Modern security demos often stop at model training. ACDS goes further by connecting:

- live network observation
- real-time inference
- defensive response hooks
- adaptive online learning
- dashboard-driven visibility

It is both an engineering project and a presentation layer for cyber defense workflows.

---

## Core Modules

### Detection Engine
- Loads a trained offline detection model for fast inference.
- Uses a saved scaler and encoder for consistent predictions.
- Supports runtime schema alignment for live traffic features.

### Online Learning Layer
- Loads a persistent incremental model.
- Updates the model when confidence thresholds are met.
- Stores learned state for future execution.

### Traffic Intelligence Pipeline
- Sniffs packets and groups them into flows.
- Extracts runtime traffic features from observed network behavior.
- Feeds transformed flow data into the AI pipeline.

### Defense Layer
- Contains firewall response hooks for IP blocking.
- Logs detections and containment actions into a unified event stream.

### Command Center Dashboard
- Advanced Streamlit interface with telemetry panels and cyber-themed visuals.
- Shows detection volume, threat mix, recent events, blocked IPs, and alert feed.

### Simulation Layer
- Generates synthetic attack events for testing, demos, and UI validation.

---

## High-Level Architecture

```text
                         +----------------------------------+
                         |         Network Traffic          |
                         +----------------+-----------------+
                                          |
                                          v
                         +----------------------------------+
                         |     Sniffer / Flow Extractor     |
                         +----------------+-----------------+
                                          |
                                          v
                         +----------------------------------+
                         |      Feature Engineering Grid    |
                         +----------------+-----------------+
                                          |
                                          v
                         +----------------------------------+
                         | Scaler + Detection Model + Label |
                         +----------------+-----------------+
                                          |
                     +--------------------+--------------------+
                     |                                         |
                     v                                         v
          +--------------------------+              +--------------------------+
          |   Firewall / Response    |              |   Online Learning Loop   |
          +------------+-------------+              +------------+-------------+
                       |                                         |
                       +--------------------+--------------------+
                                            |
                                            v
                          +--------------------------------------+
                          | Logs / Dashboard / Operator View     |
                          +--------------------------------------+
```

---

## Command Center Preview

The dashboard is designed around a futuristic SOC aesthetic:

- immersive dark control-room styling
- real-time KPI cards
- attack mix charts
- event timelines
- containment tracking
- rolling detection feed

It is intended to feel less like a generic analytics page and more like an active cyber operations console.

---

## Repository Layout

```text
ACDS/
|-- backend/
|   |-- defense/
|   |   `-- firewall.py
|   |-- detection/
|   |   |-- detect.py
|   |   `-- train_detection_model.py
|   |-- network/
|   |   |-- features.py
|   |   |-- flow_extractor.py
|   |   `-- sniffer.py
|   |-- online_learning/
|   |   |-- init_online_model.py
|   |   |-- online_model.py
|   |   `-- update.py
|   |-- utils/
|   |   |-- logger.py
|   |   `-- preprocessing.py
|   `-- main_pipeline.py
|-- dashboard/
|   `-- dashboard.py
|-- logs/
|-- models/
|   `-- generate_models.py
|-- scripts/
|   |-- run_backend.py
|   |-- run_sniffer.py
|   `-- simulate_attack.py
|-- requirements.txt
`-- README.md
```

---

## Quick Start

### 1. Create the environment

```powershell
python -m venv acds_env
.\acds_env\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the backend pipeline

```powershell
python scripts/run_backend.py
```

### 3. Start packet sniffing

```powershell
python scripts/run_sniffer.py
```

### 4. Launch the dashboard

```powershell
streamlit run dashboard/dashboard.py
```

### 5. Generate simulated attack activity

```powershell
python scripts/simulate_attack.py
```

---

## Runtime Flow

```text
1. Packets are observed
2. Flows are built and timed
3. Features are computed
4. Features are aligned to the trained schema
5. The detection model classifies the flow
6. Suspicious behavior can trigger response logic
7. High-confidence samples feed the online learner
8. Logs stream into the dashboard
```

---

## Platform Notes

### Windows Packet Capture

For sniffing on Windows, install:

- Npcap
- enable `WinPcap-compatible mode`

### Logging

- events are written to `logs/acds.log`
- dashboard panels are driven from this shared log stream
- UTF-8-safe logging is used for improved Windows compatibility

### Models

The project currently uses:

- `models/detection_model.pkl`
- `models/scaler.pkl`
- `models/encoder.pkl`
- `models/online_model.pkl`

Path handling has been stabilized to load from the repository root instead of depending on the current shell directory.

---

## Recent Improvements

- upgraded the dashboard into a more advanced cyber operations UI
- fixed Windows-safe logging and encoding issues
- stabilized path handling for models and logs
- improved sniffer launch behavior through the active Python interpreter
- added graceful handling for missing packet capture support
- aligned preprocessing with the trained scaler schema
- improved simulator logging compatibility

---

## Roadmap

- richer flow feature extraction to reduce zero-filled model inputs
- structured persistence for alerts and detections
- analyst filters and search within the dashboard
- model confidence visualizations
- IP intelligence enrichment and geolocation overlays
- multi-source telemetry ingestion
- drill-down panels for threat investigation

---

## Tech Stack

- Python
- Streamlit
- Scapy
- Pandas
- Joblib
- Scikit-learn
- XGBoost

---

## Use Cases

- cybersecurity academic projects
- intrusion detection demos
- machine learning security showcases
- blue-team themed portfolios
- real-time dashboard demonstrations

---

## Futuristic Console Sequence

```text
> booting acds core...
> synchronizing anomaly filters...
> loading trained defense models...
> opening telemetry channels...
> monitoring ingress vectors...
> threat lattice active...
> command center online...
```

---

## License

This repository currently does not include a dedicated license file. Add one before public open-source distribution if needed.

from collections import Counter
from pathlib import Path
import re
import time

import pandas as pd
import streamlit as st


st.set_page_config(page_title="ACDS Command Center", layout="wide")

LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "acds.log"
DETECTED_RE = re.compile(
    r"\[(?P<timestamp>[^\]]+)\]\s+(?P<prefix>\[SIMULATION\]\s+)?Detected:\s+(?P<ip>[^\s]+)\s+->\s+(?P<label>.+)"
)
BLOCKED_RE = re.compile(
    r"\[(?P<timestamp>[^\]]+)\]\s+(?P<prefix>\[SIMULATION\]\s+)?Blocking IP:\s+(?P<ip>.+)"
)


def load_logs():
    if not LOG_FILE.exists():
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse_logs(lines):
    detections = []
    blocked = []
    raw_events = []

    for line in lines:
        detected_match = DETECTED_RE.match(line)
        blocked_match = BLOCKED_RE.match(line)

        if detected_match:
            event = detected_match.groupdict()
            event["simulated"] = bool(event.get("prefix"))
            detections.append(event)
            raw_events.append(
                {
                    "timestamp": event["timestamp"],
                    "event": "Detection",
                    "detail": f'{event["ip"]} -> {event["label"]}',
                    "severity": "High" if event["label"] != "BENIGN" else "Info",
                }
            )
            continue

        if blocked_match:
            event = blocked_match.groupdict()
            event["simulated"] = bool(event.get("prefix"))
            blocked.append(event)
            raw_events.append(
                {
                    "timestamp": event["timestamp"],
                    "event": "Blocked",
                    "detail": event["ip"],
                    "severity": "Critical",
                }
            )
            continue

        raw_events.append(
            {
                "timestamp": line[1:20] if line.startswith("[") else "Unknown",
                "event": "System",
                "detail": line,
                "severity": "Info",
            }
        )

    return detections, blocked, raw_events


def build_timeseries(detections, blocked):
    time_buckets = Counter()

    for event in detections:
        time_buckets[event["timestamp"][:16]] += 1

    activity = (
        pd.DataFrame(
            [{"minute": minute, "detections": count} for minute, count in sorted(time_buckets.items())]
        )
        if time_buckets
        else pd.DataFrame(columns=["minute", "detections"])
    )

    blocked_df = (
        pd.DataFrame(blocked)[["timestamp", "ip"]].rename(columns={"timestamp": "time", "ip": "blocked_ip"})
        if blocked
        else pd.DataFrame(columns=["time", "blocked_ip"])
    )

    return activity, blocked_df


def render_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(18, 91, 78, 0.18), transparent 30%),
                radial-gradient(circle at top right, rgba(192, 58, 43, 0.16), transparent 28%),
                linear-gradient(135deg, #08141a 0%, #0c1f29 45%, #102f2a 100%);
            color: #e9f4ef;
        }
        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 1.5rem;
        }
        .hero {
            padding: 1.6rem 1.8rem;
            border: 1px solid rgba(138, 202, 183, 0.18);
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(5, 18, 28, 0.88), rgba(13, 54, 46, 0.82));
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
            margin-bottom: 1rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.5rem;
            letter-spacing: 0.03em;
            color: #f3fff9;
        }
        .hero p {
            margin: 0.65rem 0 0 0;
            color: #b7d2cb;
            font-size: 1rem;
            max-width: 52rem;
        }
        .metric-card {
            padding: 1rem 1.1rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(6, 16, 24, 0.7);
            backdrop-filter: blur(10px);
            min-height: 136px;
        }
        .metric-label {
            color: #9bb8b0;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #f8fffc;
            margin-top: 0.3rem;
        }
        .metric-subtext {
            margin-top: 0.6rem;
            color: #c3d8d2;
            font-size: 0.92rem;
        }
        .panel-title {
            color: #f4fff9;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.55rem;
        }
        [data-testid="stDataFrame"], [data-testid="stMetric"] {
            border-radius: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, subtext):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_live_content(container):
    lines = load_logs()
    detections, blocked, raw_events = parse_logs(lines)
    activity_df, blocked_df = build_timeseries(detections, blocked)

    attack_counts = Counter(event["label"] for event in detections if event["label"] != "BENIGN")
    top_attack = attack_counts.most_common(1)[0][0] if attack_counts else "None"
    latest_alert = detections[-1]["label"] if detections else "No traffic yet"
    blocked_unique = len({event["ip"] for event in blocked})

    with container.container():
        st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

        metric_cols = st.columns(4)
        with metric_cols[0]:
            metric_card("Detections", len(detections), "Total detection events captured from backend logs.")
        with metric_cols[1]:
            metric_card("Blocked IPs", blocked_unique, "Unique sources that triggered a containment action.")
        with metric_cols[2]:
            metric_card("Top Threat", top_attack, "Most frequent non-benign label observed so far.")
        with metric_cols[3]:
            metric_card("Latest Alert", latest_alert, "Most recent model verdict written to the log stream.")

        left, right = st.columns([1.7, 1.1])

        with left:
            st.markdown('<div class="panel-title">Detection Volume</div>', unsafe_allow_html=True)
            if activity_df.empty:
                st.info("No detections yet. Start the backend or attack simulator to populate live activity.")
            else:
                chart_df = activity_df.set_index("minute")
                st.area_chart(chart_df, color="#45c486")

        with right:
            st.markdown('<div class="panel-title">Threat Mix</div>', unsafe_allow_html=True)
            if attack_counts:
                threat_df = pd.DataFrame(
                    {"Attack Type": list(attack_counts.keys()), "Count": list(attack_counts.values())}
                ).set_index("Attack Type")
                st.bar_chart(threat_df, color="#ff6b57")
            else:
                st.info("Only benign or system events are present right now.")

        table_left, table_right = st.columns([1.3, 1])

        with table_left:
            st.markdown('<div class="panel-title">Recent Security Events</div>', unsafe_allow_html=True)
            events_df = pd.DataFrame(raw_events[-20:]).iloc[::-1] if raw_events else pd.DataFrame(
                columns=["timestamp", "event", "detail", "severity"]
            )
            st.dataframe(events_df, use_container_width=True, hide_index=True)

        with table_right:
            st.markdown('<div class="panel-title">Containment Actions</div>', unsafe_allow_html=True)
            if blocked_df.empty:
                st.info("No blocked IPs yet.")
            else:
                st.dataframe(blocked_df.iloc[::-1].head(12), use_container_width=True, hide_index=True)

        st.markdown('<div class="panel-title">Detection Feed</div>', unsafe_allow_html=True)

        if detections:
            for event in reversed(detections[-8:]):
                tone = st.error if event["label"] != "BENIGN" else st.info
                tone(f'{event["timestamp"]} | {event["ip"]} -> {event["label"]}')
        else:
            st.info("The detection feed will appear here once new traffic is processed.")


render_styles()

with st.sidebar:
    st.markdown("### Control Tower")
    auto_refresh = st.checkbox("Auto refresh", value=True)
    refresh_seconds = st.slider("Refresh interval (seconds)", min_value=2, max_value=10, value=2)
    st.button("Refresh now", use_container_width=True)

lines = load_logs()
detections, blocked, raw_events = parse_logs(lines)
activity_df, blocked_df = build_timeseries(detections, blocked)

attack_counts = Counter(event["label"] for event in detections if event["label"] != "BENIGN")
top_attack = attack_counts.most_common(1)[0][0] if attack_counts else "None"
latest_alert = detections[-1]["label"] if detections else "No traffic yet"
blocked_unique = len({event["ip"] for event in blocked})

st.markdown(
    """
    <div class="hero">
        <h1>ACDS Cyber Defense Command Center</h1>
        <p>
            Live monitoring for detections, containment actions, and traffic behavior.
            The view refreshes automatically so you can keep an eye on the system while attacks are simulated or captured.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

live_container = st.empty()
render_live_content(live_container)

if auto_refresh:
    while True:
        time.sleep(refresh_seconds)
        render_live_content(live_container)

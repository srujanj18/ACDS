import time

flows = {}


def get_flow_key(packet):
    try:
        src = packet["IP"].src
        dst = packet["IP"].dst
        proto = packet["IP"].proto

        sport = 0
        dport = 0

        if packet.haslayer("TCP"):
            sport = packet["TCP"].sport
            dport = packet["TCP"].dport

        elif packet.haslayer("UDP"):
            sport = packet["UDP"].sport
            dport = packet["UDP"].dport

        return (src, dst, sport, dport, proto)

    except:
        return None


def update_flow(packet):
    key = get_flow_key(packet)

    if key is None:
        return None

    if key not in flows:
        flows[key] = {
            "start_time": packet.time,
            "packet_count": 0,
            "byte_count": 0,
            "packet_lengths": [],
            "timestamps": []
        }

    flow = flows[key]

    flow["packet_count"] += 1
    flow["byte_count"] += len(packet)
    flow["packet_lengths"].append(len(packet))
    flow["timestamps"].append(packet.time)

    return key


def get_completed_flows(timeout=10):
    """
    Return flows that are inactive for given timeout
    """
    completed = []

    current_time = time.time()

    for key in list(flows.keys()):
        flow = flows[key]

        if current_time - flow["timestamps"][-1] > timeout:
            completed.append((key, flow))
            del flows[key]

    return completed
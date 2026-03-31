import os
import platform

blocked_ips = set()


def block_ip(ip):
    if ip in blocked_ips:
        return

    print(f"🚫 Blocking IP: {ip}")
    blocked_ips.add(ip)

    system = platform.system()

    try:
        if system == "Linux":
            os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")

        elif system == "Windows":
            os.system(f'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block remoteip={ip}')

        else:
            print("⚠️ Unsupported OS for firewall")

    except Exception as e:
        print("❌ Firewall error:", e)


def get_blocked_ips():
    return list(blocked_ips)
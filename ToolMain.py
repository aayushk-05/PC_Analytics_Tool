from flask import Flask, jsonify, send_from_directory
import psutil, os, signal, GPUtil

app = Flask(__name__)


# ================= FRONTEND =================

@app.route("/")
def index():
    return send_from_directory(".", "altgui.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)


# ================= STATS =================

@app.route("/stats")
def stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    # temperature
    temp = 0
    try:
        temps = psutil.sensors_temperatures()
        for _, e in temps.items():
            temp = e[0].current
            break
    except:
        pass

    # GPU
    try:
        g = GPUtil.getGPUs()[0]
        gpu = g.load * 100
    except:
        gpu = 0

    # disks
    disks = []
    for d in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(d.mountpoint).percent
            disks.append({"mount": d.mountpoint, "usage": usage})
        except:
            pass

    return jsonify({
        "cpu": cpu,
        "ram": ram,
        "gpu": gpu,
        "temp": temp,
        "disks": disks
    })


# ================= PROCESSES =================

@app.route("/processes")
def processes():
    procs = sorted(
        [(p.info['pid'], p.info['name'], p.info['cpu_percent'])
         for p in psutil.process_iter(['pid','name','cpu_percent'])],
        key=lambda x: x[2],
        reverse=True
    )[:10]

    return jsonify(procs)


# ================= KILL =================

@app.route("/kill/<int:pid>")
def kill(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        return {"status": "killed"}
    except:
        return {"status": "failed"}


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)

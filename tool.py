import psutil
import GPUtil
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
import pyqtgraph as pg


class Monitor(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PC Analytics Tool (Afterburner Style)")
        self.resize(1200, 800)

        pg.setConfigOptions(background="#111111", foreground="white")

        # rolling graph buffers
        self.cpu_data = [0]*120
        self.ram_data = [0]*120
        self.gpu_data = [0]*120
        self.temp_data = [0]*120

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(500)


    # ---------------- UI ----------------
    def init_ui(self):
        layout = QGridLayout(self)

        self.cpu_plot = self.make_plot("CPU %")
        self.ram_plot = self.make_plot("RAM %")
        self.gpu_plot = self.make_plot("GPU %")
        self.temp_plot = self.make_plot("Temp °C")

        layout.addWidget(self.cpu_plot, 0, 0)
        layout.addWidget(self.ram_plot, 0, 1)
        layout.addWidget(self.gpu_plot, 1, 0)
        layout.addWidget(self.temp_plot, 1, 1)

        # Disk usage
        self.disk_label = QLabel()
        self.disk_label.setStyleSheet("color:white;font-size:14px;")
        layout.addWidget(self.disk_label, 2, 0)

        # Process table
        self.proc_table = QTableWidget(0, 3)
        self.proc_table.setHorizontalHeaderLabels(["PID", "Name", "CPU%"])
        self.proc_table.setStyleSheet("background:#222;color:white;")
        layout.addWidget(self.proc_table, 2, 1)

        # Kill process
        kill_layout = QHBoxLayout()
        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("Enter PID")

        kill_btn = QPushButton("Kill Process")
        kill_btn.clicked.connect(self.kill_process)

        kill_layout.addWidget(self.pid_input)
        kill_layout.addWidget(kill_btn)

        layout.addLayout(kill_layout, 3, 0, 1, 2)


    # ---------------- Plot ----------------
    def make_plot(self, title):
        plot = pg.PlotWidget(title=title)
        plot.setYRange(0, 100)
        plot.showGrid(x=True, y=True)
        plot.setMouseEnabled(False, False)
        return plot


    # ---------------- Helpers ----------------
    def cpu_temp(self):
        try:
            temps = psutil.sensors_temperatures()
            for _, e in temps.items():
                return e[0].current
        except:
            return 0


    def gpu_usage(self):
        try:
            return GPUtil.getGPUs()[0].load * 100
        except:
            return 0


    # ---------------- Update loop ----------------
    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        gpu = self.gpu_usage()
        temp = self.cpu_temp()

        self.push(self.cpu_data, cpu)
        self.push(self.ram_data, ram)
        self.push(self.gpu_data, gpu)
        self.push(self.temp_data, temp)

        self.cpu_plot.plot(self.cpu_data, clear=True)
        self.ram_plot.plot(self.ram_data, clear=True)
        self.gpu_plot.plot(self.gpu_data, clear=True)
        self.temp_plot.plot(self.temp_data, clear=True)

        self.update_disks()
        self.update_process_table()


    # ---------------- Disk ----------------
    def update_disks(self):
        text = ""
        for p in psutil.disk_partitions():
            try:
                u = psutil.disk_usage(p.mountpoint).percent
                text += f"{p.mountpoint}: {u}%   "
            except:
                pass
        self.disk_label.setText(text)


    # ---------------- Processes ----------------
    def update_process_table(self):
        procs = sorted(
            [(p.info['pid'], p.info['name'], p.info['cpu_percent'])
             for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])],
            key=lambda x: x[2],
            reverse=True
        )[:8]

        self.proc_table.setRowCount(len(procs))

        for r, (pid, name, cpu) in enumerate(procs):
            self.proc_table.setItem(r, 0, QTableWidgetItem(str(pid)))
            self.proc_table.setItem(r, 1, QTableWidgetItem(name))
            self.proc_table.setItem(r, 2, QTableWidgetItem(str(cpu)))


    # ---------------- Kill ----------------
    def kill_process(self):
        try:
            pid = int(self.pid_input.text())
            psutil.Process(pid).kill()
        except:
            pass


    # ---------------- Buffer ----------------
    def push(self, arr, val):
        arr.pop(0)
        arr.append(val)

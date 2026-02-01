
PC Analytics Tool

A modern real-time system monitoring dashboard built using Python (Flask) + HTML + CSS + JavaScript.
This tool works like a lightweight Task Manager + MSI Afterburner, showing live system statistics directly in your browser with smooth charts and a clean dark UI.

Perfect for:

🧠 Learning Flask
🖥 Monitoring system performance
🧪 Practicing frontend + backend integration
⚙️ Building analytics dashboards

✨ Features

📊 Live Monitoring

CPU Usage (%)
RAM Usage (%)
GPU Usage (%)
CPU Temperature
Disk Usage

📈 Real-Time Graphs
Auto-updating charts
Smooth scrolling
1-second refresh rate

⚙️ Process Manager
View top running processes
Sort by CPU usage
Kill any process instantly

🎨 Clean UI
Dark theme
Card-based layout
MSI Afterburner inspired look
Fully browser-based

🛠 Tech Stack
Backend
Python
Flask
psutil
GPUtil
Frontend
HTML
CSS
JavaScript
Chart.js

📁 Project Structure
PC_Analytics_Tool/
│
├── ToolMain.py        → Flask backend server
├── altgui.html        → Main frontend page
├── style.css          → Styling and theme
├── app.js             → Charts and API logic
├── requirements.txt   → Dependencies
└── README.md

⚙️ Installation Guide
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/PC_Analytics_Tool.git
cd PC_Analytics_Tool

2️⃣ Create virtual environment (recommended)
Linux / macOS
python3 -m venv venv
source venv/bin/activate

Windows
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies

If requirements.txt exists:
pip install -r requirements.txt

Or manually:
pip install flask psutil gputil setuptools

▶️ Run the App
Linux / macOS
python3 ToolMain.py

Windows
python ToolMain.py

🌐 Open in Browser

After running, open:

http://127.0.0.1:5000
Your dashboard will load instantly.

🧠 How It Works

The Flask backend provides APIs:

/stats        → system metrics (CPU, RAM, GPU)
/processes    → running processes
/kill/<pid>   → terminate process


The frontend fetches this data every second using JavaScript and updates charts live.

🐛 Common Fixes

Flask not found
pip install flask

psutil not found
pip install psutil

Linux pip restriction error

Use virtual environment:

python3 -m venv venv
source venv/bin/activate

🚀 Future Improvements (Ideas)

Per-core CPU graphs
GPU temperature monitoring
Fan speed stats
System alerts
Log exporting
Desktop (.exe) app
Android APK version
Electron build

🎯 Why this Project?
This project helped me learn:

Flask backend APIs
Frontend dashboards
System monitoring with Python
Real-time data visualization
Full-stack integration
Great for beginners and portfolio projects.

Developed with ❤️ by
Aayush Khugshal

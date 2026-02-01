import sys
from PyQt6.QtWidgets import QApplication
from tool import Monitor

app = QApplication(sys.argv)
window = Monitor()
window.show()
sys.exit(app.exec())

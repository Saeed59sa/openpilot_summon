# sdracemode_ui.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

def launch():
    app = QApplication(sys.argv)
    window = SDRaceModeUI()
    window.show()
    sys.exit(app.exec_())

class SDRaceModeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SDRaceMode Interface")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        label = QLabel("✅ SDRaceMode is active!", self)
        layout.addWidget(label)

        close_btn = QPushButton("Close", self)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

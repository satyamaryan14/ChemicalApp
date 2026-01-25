import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Analytics (Desktop)")
        self.setGeometry(100, 100, 600, 700)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 1. Header
        self.label = QLabel("Step 1: Upload a CSV File")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.label)

        # 2. Upload Button
        self.btn = QPushButton("Select & Analyze CSV")
        self.btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px; font-weight: bold;")
        self.btn.clicked.connect(self.upload_file)
        layout.addWidget(self.btn)

        # 3. Stats Display Area
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("padding: 10px; border: 1px solid #ddd; background: #f9f9f9;")
        layout.addWidget(self.stats_label)

        # 4. Chart Area (Matplotlib embedded in PyQt)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def upload_file(self):
        # Open File Picker
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')
        
        if fname:
            self.label.setText("Analyzing... Please wait.")
            try:
                # Send file to Django (Connecting Desktop to Web!)
                files = {'file': open(fname, 'rb')}
                response = requests.post('http://127.0.0.1:8000/api/upload/', files=files)
                
                if response.status_code == 200:
                    data = response.json()['stats']
                    self.update_dashboard(data)
                else:
                    self.show_error("Server Error! Is Django running?")
            except Exception as e:
                self.show_error(f"Connection Failed: {e}")

    def update_dashboard(self, stats):
        # Update Text
        self.label.setText("Analysis Complete")
        info = (f"Total Equipment: {stats['total_count']}\n"
                f"Avg Pressure: {stats['avg_pressure']} bar\n"
                f"Avg Temp: {stats['avg_temp']} C")
        self.stats_label.setText(info)

        # Update Chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(stats['chart_labels'], stats['chart_data'], color='orange') # Orange to distinguish from Web's Blue
        ax.set_title("Equipment Distribution")
        ax.set_ylabel("Count")
        self.canvas.draw()

    def show_error(self, msg):
        QMessageBox.critical(self, "Error", msg)
        self.label.setText("Ready")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesktopApp()
    ex.show()
    sys.exit(app.exec_())
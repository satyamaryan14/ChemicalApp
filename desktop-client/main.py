import sys
import requests
import matplotlib
# Force Qt5 Backend
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox, QListWidget, QLineEdit, QDialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_BASE_URL = "http://127.0.0.1:8000/api"

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)
        self.token = None

    def handle_login(self):
        try:
            response = requests.post(f"{API_BASE_URL}/login/", 
                                   json={"username": self.username_input.text(), "password": self.password_input.text()},
                                   timeout=5)
            if response.status_code == 200:
                self.token = response.json().get("token")
                self.accept()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot connect to server.\n{e}")

class DashboardWindow(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle("Chemical Equipment Dashboard")
        self.setGeometry(100, 100, 900, 700)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Step 1: Upload Equipment Data (CSV)"))
        
        self.upload_btn = QPushButton("Select CSV & Analyze")
        self.upload_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.upload_btn.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_btn)

        self.stats_label = QLabel("Statistics: Waiting for data...")
        self.stats_label.setStyleSheet("font-weight: bold; font-size: 14px; margin: 10px;")
        self.layout.addWidget(self.stats_label)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Ready to Upload")
        self.ax.text(0.5, 0.5, "No Data Yet", ha='center')

        self.layout.addWidget(QLabel("Recent Uploads:"))
        self.history_list = QListWidget()
        self.layout.addWidget(self.history_list)
        self.setLayout(self.layout)
        self.load_history()

    def load_history(self):
        try:
            headers = {"Authorization": f"Token {self.token}"}
            res = requests.get(f"{API_BASE_URL}/history/", headers=headers, timeout=3)
            if res.status_code == 200:
                self.history_list.clear()
                for item in res.json():
                    self.history_list.addItem(f"{item['filename']} ({item['uploaded_at'][:10]})")
        except:
            pass

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not fname: return
        self.stats_label.setText("Processing... Please wait...")
        QApplication.processEvents()

        try:
            headers = {"Authorization": f"Token {self.token}"}
            files = {'file': open(fname, 'rb')}
            response = requests.post(f"{API_BASE_URL}/upload/", headers=headers, files=files, timeout=10)
            
            if response.status_code == 201:
                data = response.json()
                self.update_ui(data)
                self.load_history()
            else:
                QMessageBox.warning(self, "Upload Failed", f"Server Error: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Processing Error: {str(e)}")

    def update_ui(self, root_data):
        # Flatten the data structure if 'stats' is nested
        data = root_data.get('stats', root_data)

        # 1. Get Stats (Safely)
        count = data.get('total_count', 0)
        pressure = data.get('avg_pressure', 0.0)
        temp = data.get('avg_temp', 0.0)

        self.stats_label.setText(f"Analyzed {count} items. Avg Pressure: {pressure:.2f} | Temp: {temp:.2f}")

        # 2. Get Chart Data (Using the Correct Keys from your Terminal Log)
        labels = data.get('chart_labels', [])
        
        # FIX: Check for 'chart_data' OR 'chart_counts'
        counts = data.get('chart_data', [])
        if not counts:
            counts = data.get('chart_counts', [])

        # 3. Draw Chart
        self.ax.clear()
        if labels and counts:
            bars = self.ax.bar(labels, counts, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
            self.ax.set_title("Equipment Distribution")
            self.ax.bar_label(bars)
            self.ax.tick_params(axis='x', rotation=45)
            self.figure.tight_layout()
        else:
            self.ax.text(0.5, 0.5, "No Chart Data Found", ha='center')
        
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        window = DashboardWindow(login.token)
        window.show()
        sys.exit(app.exec_())
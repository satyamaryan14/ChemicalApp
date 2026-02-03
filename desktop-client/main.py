import sys
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox, QHBoxLayout, QFrame, QListWidget, QSizePolicy, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# --- SAFE IMPORT FOR MATERIAL DESIGN ---
try:
    from qt_material import apply_stylesheet
    MATERIAL_AVAILABLE = True
except ImportError:
    MATERIAL_AVAILABLE = False

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api"

class ChemicalApp(QWidget):
    def __init__(self):
        super().__init__()
        self.token = None
        self.initUI()
        self.plot_data({}) 

    def initUI(self):
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        if not MATERIAL_AVAILABLE:
            self.setStyleSheet("background-color: #f5f5f5;")

        main_layout = QHBoxLayout()
        
        # --- LEFT SIDE: CHART ---
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 10, 0)
        
        self.header = QLabel("Real-time Sensor Analytics")
        self.header.setFont(QFont('Segoe UI', 20, QFont.Bold)) 
        left_layout.addWidget(self.header)

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.figure.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.1)
        self.figure.patch.set_facecolor('none') 
        
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setStyleSheet("background-color:transparent;")
        left_layout.addWidget(self.canvas)
        
        self.status_label = QLabel("Status: Not Logged In")
        self.status_label.setStyleSheet("font-size: 14px; margin-top: 5px;")
        left_layout.addWidget(self.status_label)

        main_layout.addLayout(left_layout, 7)

        # --- RIGHT SIDE: SIDEBAR ---
        right_frame = QFrame()
        if not MATERIAL_AVAILABLE:
            right_frame.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 8px;")
        
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)

        # --- NEW: LOGIN INPUT FIELDS ---
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.user_input.setText("aryan") # Default text for demo
        right_layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password) # Hides password with ***
        self.pass_input.setText("pass1234") # Default text for demo
        right_layout.addWidget(self.pass_input)

        # 1. Login Button
        self.login_btn = QPushButton("Login to Server")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.login)
        if MATERIAL_AVAILABLE:
            self.login_btn.setProperty('class', 'primary')
        else:
            self.login_btn.setStyleSheet("background-color: #1a237e; color: white; padding: 10px; border-radius: 5px;")
        right_layout.addWidget(self.login_btn)

        # 2. Upload Button
        self.upload_btn = QPushButton("UPLOAD CSV DATA")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        if MATERIAL_AVAILABLE:
            self.upload_btn.setProperty('class', 'success')
        else:
            self.upload_btn.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; border-radius: 5px;")
        self.upload_btn.setFixedHeight(50)
        right_layout.addWidget(self.upload_btn)

        # 3. History List
        history_label = QLabel("Recent Uploads")
        history_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        history_label.setStyleSheet("border: none; margin-top: 10px;")
        right_layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_chart_from_history)
        right_layout.addWidget(self.history_list)

        main_layout.addWidget(right_frame, 3)
        self.setLayout(main_layout)

    def login(self):
        # --- GET CREDENTIALS FROM INPUT BOXES ---
        username = self.user_input.text()
        password = self.pass_input.text()

        try:
            response = requests.post(f"{API_URL}/login/", data={"username": username, "password": password})
            if response.status_code == 200:
                self.token = response.json()['token']
                self.status_label.setText(f"Status: Logged in as {username}")
                self.login_btn.setText("Logged In ✓")
                self.login_btn.setEnabled(False)
                # Hide inputs after login for cleaner look
                self.user_input.setVisible(False)
                self.pass_input.setVisible(False)
                
                self.upload_btn.setEnabled(True)
                self.fetch_history()
                QMessageBox.information(self, "Success", "Connected to Hybrid Backend!")
            else:
                QMessageBox.warning(self, "Login Failed", f"Server said: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Is Django running?\n{str(e)}")

    def fetch_history(self):
        if not self.token: return
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f"{API_URL}/history/", headers=headers)
            if response.status_code == 200:
                self.history_data = response.json()
                self.history_list.clear()
                for item in self.history_data:
                    name = item.get('filename', 'Unknown').replace('.csv', '')
                    self.history_list.addItem(f"📄 {name}")
                if self.history_data:
                    self.plot_data(self.history_data[0])
        except Exception as e:
            print(f"Error fetching history: {e}")

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', 'c:\\', "CSV Files (*.csv)")
        if fname:
            try:
                files = {'file': open(fname, 'rb')}
                headers = {'Authorization': f'Token {self.token}'}
                response = requests.post(f"{API_URL}/upload/", files=files, headers=headers)
                if response.status_code == 201:
                    QMessageBox.information(self, "Success", "Data Uploaded to Cloud!")
                    self.fetch_history()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def load_chart_from_history(self, item):
        row = self.history_list.row(item)
        data = self.history_data[row]
        self.plot_data(data)

    def plot_data(self, data):
        self.ax.clear()
        
        fid = data.get('id', 1)
        stats = data.get('stats', {})
        chart_labels = stats.get('chart_labels', ['Pressure', 'Temp', 'Flow', 'Viscosity'])
        chart_data = stats.get('chart_data', [65, 59, 80, 45])

        # Create Bar Chart
        self.ax.bar(chart_labels, chart_data, color=['#1976d2', '#d32f2f', '#388e3c', '#fbc02d'])
        self.ax.axhline(y=85, color='red', linestyle='--', label='Safety Limit')
        
        filename = data.get('filename', 'Demo Mode')
        self.ax.set_title(f"Analysis: {filename}", fontsize=12)
        self.ax.set_ylabel("Sensor Units")
        self.ax.legend()
        self.ax.grid(axis='y', linestyle=':', alpha=0.7)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # --- APPLY MATERIAL THEME IF AVAILABLE ---
    if MATERIAL_AVAILABLE:
        apply_stylesheet(app, theme='light_blue.xml')
        
    ex = ChemicalApp()
    ex.show()
    sys.exit(app.exec_())
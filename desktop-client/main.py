import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox, QHBoxLayout, QFrame, QListWidget)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api"
THEME_COLOR = "#1a237e"  # Matches your React App Navbar

class ChemicalApp(QWidget):
    def __init__(self):
        super().__init__()
        self.token = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop Client)")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f5f5f5;") # Light Grey Background

        # Main Layout
        main_layout = QHBoxLayout()
        
        # --- LEFT SIDE: CHART (75%) ---
        left_layout = QVBoxLayout()
        
        # Header
        self.header = QLabel("Real-time Sensor Analytics")
        self.header.setFont(QFont('Segoe UI', 16, QFont.Bold))
        self.header.setStyleSheet(f"color: {THEME_COLOR}; margin-bottom: 10px;")
        left_layout.addWidget(self.header)

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.figure.patch.set_facecolor('#f5f5f5') # Match background
        left_layout.addWidget(self.canvas)
        
        # Login/Status Frame
        self.status_label = QLabel("Status: Not Logged In")
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        left_layout.addWidget(self.status_label)

        main_layout.addLayout(left_layout, 7) # Stretch factor 7

        # --- RIGHT SIDE: SIDEBAR (25%) ---
        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #ddd;")
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)

        # 1. Login Button
        self.login_btn = QPushButton("Login to Server")
        self.style_button(self.login_btn, is_primary=False)
        self.login_btn.clicked.connect(self.login)
        right_layout.addWidget(self.login_btn)

        # 2. Upload Button (Big Blue)
        self.upload_btn = QPushButton(" UPLOAD CSV")
        self.style_button(self.upload_btn, is_primary=True)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False) # Disabled until login
        right_layout.addWidget(self.upload_btn)

        # 3. History List
        history_label = QLabel("Recent Uploads")
        history_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        history_label.setStyleSheet("border: none; margin-top: 20px;")
        right_layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget { border: 1px solid #eee; border-radius: 5px; padding: 5px; }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #eee; }
            QListWidget::item:selected { background-color: #e3f2fd; color: #1565c0; }
        """)
        self.history_list.itemClicked.connect(self.load_chart_from_history)
        right_layout.addWidget(self.history_list)

        # Add right frame to main layout
        main_layout.addWidget(right_frame, 3) # Stretch factor 3

        self.setLayout(main_layout)

    def style_button(self, button, is_primary=True):
        bg_color = THEME_COLOR if is_primary else "#ffffff"
        text_color = "#ffffff" if is_primary else THEME_COLOR
        border = "none" if is_primary else f"2px solid {THEME_COLOR}"
        
        button.setFont(QFont('Segoe UI', 10, QFont.Bold))
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedHeight(45)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: {border};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {'#283593' if is_primary else '#f0f4c3'};
            }}
        """)

    def login(self):
        # Hardcoded for the demo video speed (or popup a dialog)
        # In a real app, you'd use QInputDialog
        username = "admin" 
        password = "pass1234" # Make sure this matches your createsuperuser!
        
        try:
            response = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
            if response.status_code == 200:
                self.token = response.json()['token']
                self.status_label.setText(f"Status: Logged in as {username}")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.login_btn.setText("Logged In ✓")
                self.login_btn.setEnabled(False)
                self.upload_btn.setEnabled(True)
                self.fetch_history()
                QMessageBox.information(self, "Success", "Connected to Hybrid Backend!")
            else:
                QMessageBox.warning(self, "Error", "Login Failed")
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
                
                # Load the first one automatically
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
        
        # Simulated data visualization based on ID
        # In a real app, you would parse the actual CSV here
        fid = data.get('id', 0)
        
        categories = ['Pressure', 'Temp', 'Flow', 'Viscosity']
        values = [65 + (fid % 20), 59 + (fid % 15), 80 - (fid % 10), 45 + (fid % 5)]
        
        # Create Bar Chart
        bars = self.ax.bar(categories, values, color=['#1976d2', '#d32f2f', '#388e3c', '#fbc02d'])
        
        # Add a threshold line
        self.ax.axhline(y=85, color='red', linestyle='--', label='Safety Limit')
        
        self.ax.set_title(f"Analysis: {data.get('filename', '')}", fontsize=12)
        self.ax.set_ylabel("Sensor Units")
        self.ax.legend()
        self.ax.grid(axis='y', linestyle=':', alpha=0.7)
        
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChemicalApp()
    ex.show()
    sys.exit(app.exec_())
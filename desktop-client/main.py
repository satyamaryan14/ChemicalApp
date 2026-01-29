import sys
import requests
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox, QListWidget, QLineEdit, QDialog)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api"

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.attempt_login)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)
        self.token = None
        self.username = None

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        try:
            # 1. Ask Server for a Token
            response = requests.post(f"{API_URL}/login/", json={
                "username": username,
                "password": password
            })
            
            if response.status_code == 200:
                self.token = response.json().get('token')
                self.username = username
                self.accept()  # Close dialog on success
            else:
                QMessageBox.warning(self, "Error", "Invalid Credentials")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Server Error! Is Django running?\n{str(e)}")

class ChemicalApp(QWidget):
    def __init__(self, token, username):
        super().__init__()
        self.token = token  # Store the permission slip
        self.username = username
        self.initUI()
        self.refresh_history()

    def initUI(self):
        self.setWindowTitle(f"Chemical Equipment Dashboard - Logged in as: {self.username}")
        self.setGeometry(100, 100, 600, 700)
        self.layout = QVBoxLayout()

        # 1. Header
        self.label = QLabel("Step 1: Upload a CSV File")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(self.label)

        # 2. Upload Button
        self.btn = QPushButton("Select & Analyze CSV")
        self.btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px; font-weight: bold;")
        self.btn.clicked.connect(self.upload_file)
        self.layout.addWidget(self.btn)

        # 3. Stats Display Area
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("padding: 10px; border: 1px solid #ddd; background: #f9f9f9;")
        self.layout.addWidget(self.stats_label)

        # 4. Chart Area
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # 5. History List
        self.history_label = QLabel("Recent Uploads (Synced):")
        self.layout.addWidget(self.history_label)
        self.history_list = QListWidget()
        self.layout.addWidget(self.history_list)

        self.setLayout(self.layout)

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')
        
        if fname:
            self.label.setText("Analyzing... Please wait.")
            try:
                files = {'file': open(fname, 'rb')}
                # CRITICAL: Send the Token!
                headers = {'Authorization': f'Token {self.token}'}
                
                response = requests.post(f"{API_URL}/upload/", files=files, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    # Check if 'stats' key exists, if not use data directly or adjust
                    stats = data.get('stats', data) 
                    
                    # Update text and chart
                    self.update_dashboard(stats)
                    self.refresh_history()
                else:
                    self.label.setText(f"Error: {response.text}")
            except Exception as e:
                self.label.setText(f"Connection Failed: {e}")

    def update_dashboard(self, stats):
        self.label.setText("Analysis Complete")
        # Handle cases where stats might be nested or direct
        total = stats.get('total_count', 0)
        avg_p = stats.get('avg_pressure', 0)
        avg_t = stats.get('avg_temp', 0)
        
        info = (f"Total Equipment: {total}\n"
                f"Avg Pressure: {avg_p} bar\n"
                f"Avg Temp: {avg_t} C")
        self.stats_label.setText(info)

        # Draw Chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Safe access to chart data
        labels = stats.get('chart_labels', [])
        values = stats.get('chart_data', [])
        
        ax.bar(labels, values, color='orange')
        ax.set_title("Equipment Distribution")
        ax.set_ylabel("Count")
        self.canvas.draw()

    def refresh_history(self):
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f"{API_URL}/history/", headers=headers)
            if response.status_code == 200:
                self.history_list.clear()
                history = response.json()
                for item in history:
                    # Handle different history formats just in case
                    name = item.get('filename', 'Unknown')
                    time = item.get('timestamp', '')
                    self.history_list.addItem(f"{name} - {time}")
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Show Login Dialog First
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        ex = ChemicalApp(login.token, login.username)
        ex.show()
        sys.exit(app.exec_())
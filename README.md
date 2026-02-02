Markdown
# Chemical Equipment Parameter Visualizer 🧪📊

A **Hybrid Web & Desktop Application** designed to visualize and analyze chemical equipment parameters. This project demonstrates a full-stack architecture where both a **React Web Client** and a **PyQt5 Desktop Client** consume a shared **Django REST Framework** backend.

---

## 🚀 Features

* **Hybrid Architecture:** Seamless synchronization between Web and Desktop platforms using a single database.
* **Data Analysis:** Upload CSV files to parse equipment data (Pressure, Temperature, Flowrate).
* **Interactive Visualization:**
    * **Desktop:** Native graphs using **Matplotlib**.
    * **Web:** Interactive charts using **Chart.js**.
* **History Management:** Automatically stores and syncs the last 5 uploaded datasets.
* **PDF Reporting:** Generate and download PDF reports of the current analytics.
* **Secure Authentication:** Token-based authentication for both client platforms.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Django + DRF | REST API, Data Parsing, Authentication |
| **Web Frontend** | React.js + Chart.js | Responsive Dashboard & Visualization |
| **Desktop Client** | PyQt5 + Matplotlib | Native GUI application for Windows/Linux |
| **Data Processing** | Pandas | Efficient CSV parsing and statistical analysis |
| **Database** | SQLite | Lightweight storage for user history |

---

## 📸 Screenshots

### 1. Web & Desktop Dashboards
![Project Screenshot](image-1.png)


---

## ⚙️ Installation & Setup Guide

This project requires **3 separate terminals** running simultaneously.

### 1. Backend Setup (Django) 🧠
*Open Terminal 1*
```bash
cd backend

# Create & Activate Virtual Environment
python -m venv venv
# Windows:
..\venv\Scripts\activate
# Mac/Linux:
source ../venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Setup Database & Admin
python manage.py migrate
python manage.py createsuperuser

# Start Server
python manage.py runserver
Server runs at: http://127.0.0.1:8000/

2. Web Client Setup (React) 🌐
Open Terminal 2

Bash
cd web-client

# Install Libraries
npm install

# Start React App
npm start
App runs at: http://localhost:3000/

3. Desktop Client Setup (PyQt5) 🖥️
Open Terminal 3

Bash
cd desktop-client

# Activate the SAME virtual environment as backend
# Windows:
..\venv\Scripts\activate
# Mac/Linux:
source ../venv/bin/activate

# Launch App
python main.py
📂 Project Structure
Bash
ChemicalApp/
├── backend/            # Django Project & API
│   ├── api/            # App logic (serializers, views)
│   ├── uploads/        # Stored CSV files
│   └── manage.py
├── web-client/         # React Application
│   ├── src/            # Components (Dashboard, Login)
│   └── package.json
├── desktop-client/     # PyQt5 Application
│   ├── main.py         # Entry point for Desktop GUI
│   └── requirements.txt
└── sample_equipment_data.csv # Test Data
👨‍💻 Author
Satyam Aryan

Submission for: Hybrid Web + Desktop Application Intern Task

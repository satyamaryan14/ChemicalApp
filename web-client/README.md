# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop)

A full-stack hybrid application designed to analyze and visualize chemical equipment data. The system consists of a **Django REST Framework** backend that serves two synchronized frontends: a **React.js Web Dashboard** and a **PyQt5 Desktop Application**.

## 🚀 Features
- **Hybrid Architecture:** Seamless synchronization between Web and Desktop clients.
- **Data Analytics:** automated parsing of CSV files to calculate average pressure, temperature, and equipment distribution.
- **Visualization:** Interactive charts using **Chart.js** (Web) and **Matplotlib** (Desktop).
- **Secure Authentication:** Token-based login system for API access.
- **Report Generation:** Auto-generated PDF reports of the latest analysis.
- **History Tracking:** Persists the last 5 uploads using SQLite.

## 🛠 Tech Stack
- **Backend:** Python, Django, Django REST Framework, Pandas
- **Frontend (Web):** React.js, Chart.js, Axios
- **Frontend (Desktop):** Python, PyQt5, Matplotlib, Requests
- **Database:** SQLite

## ⚙️ Setup Instructions

### 1. Backend Setup (Django)
```bash
cd backend
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate, Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
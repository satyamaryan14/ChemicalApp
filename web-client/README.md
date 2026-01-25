# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop)

A full-stack hybrid application that runs as both a **Web Application (React)** and a **Desktop Application (PyQt5)**, powered by a single **Django Backend**.

## 🚀 Features
- **Hybrid Architecture:** One backend serving two different frontends.
- **Analytics Engine:** Python Pandas calculates statistics (Average Pressure, Temperature).
- **Visualization:** Chart.js (Web) and Matplotlib (Desktop).

## 🛠️ Tech Stack
- **Backend:** Django REST Framework, Pandas
- **Web:** React.js, Axios, Chart.js
- **Desktop:** PyQt5, Matplotlib, Requests

## ⚙️ How to Run

### 1. Start Backend
```bash
cd ChemicalApp
venv\Scripts\activate
cd backend
python manage.py runserver
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  
  const [file, setFile] = useState(null);
  const [stats, setStats] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [history, setHistory] = useState([]);

  // Load history if logged in
  useEffect(() => {
    if (token) fetchHistory();
  }, [token]);

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/login/", { username, password });
      setToken(res.data.token);
    } catch (err) {
      alert("Invalid Credentials");
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/history/", {
        headers: { Authorization: `Token ${token}` }
      });
      setHistory(res.data);
    } catch (err) { console.error(err); }
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/upload/", formData, {
        headers: { 
            "Content-Type": "multipart/form-data",
            Authorization: `Token ${token}`
        },
      });
      setStats(res.data.stats);
      setChartData({
        labels: Object.keys(res.data.stats.type_distribution),
        datasets: [{ label: "Count", data: Object.values(res.data.stats.type_distribution), backgroundColor: "blue" }],
      });
      fetchHistory();
    } catch (err) { alert("Upload Failed"); }
  };

  const downloadPDF = () => {
    axios.get("http://127.0.0.1:8000/api/pdf/", {
        responseType: 'blob',
        headers: { Authorization: `Token ${token}` }
    }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'report.pdf');
        document.body.appendChild(link);
        link.click();
    });
  };

  // --- LOGIN SCREEN ---
  if (!token) {
    return (
      <div style={{ padding: "50px", textAlign: "center", fontFamily: "Arial" }}>
        <h2>🔐 Chemical App Login</h2>
        <input placeholder="Username" onChange={e=>setUsername(e.target.value)} style={{padding: "10px", margin: "5px"}}/><br/>
        <input type="password" placeholder="Password" onChange={e=>setPassword(e.target.value)} style={{padding: "10px", margin: "5px"}}/><br/>
        <button onClick={handleLogin} style={{padding: "10px 20px", background: "#28a745", color: "white", border: "none", cursor: "pointer"}}>Login</button>
      </div>
    );
  }

  // --- DASHBOARD SCREEN ---
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
        <h1>⚗️ Dashboard (Authorized)</h1>
        <button onClick={downloadPDF} style={{padding: "10px 20px", background: "#dc3545", color: "white", border: "none", cursor: "pointer", fontWeight: "bold"}}>
          📄 Download PDF Report
        </button>
      </div>
      <hr/>
      
      <div style={{margin: "20px 0"}}>
        <input type="file" onChange={e => setFile(e.target.files[0])} />
        <button onClick={handleUpload} style={{padding: "8px 15px", background: "#007bff", color: "white", border: "none", marginLeft: "10px"}}>Analyze CSV</button>
      </div>

      {/* CHARTS & STATS */}
      {stats && (
        <div style={{ display: "flex", marginTop: "20px", gap: "20px" }}>
            <div style={{ padding: "20px", background: "#f8f9fa", borderRadius: "8px" }}>
                <h3>Stats</h3>
                <p><strong>Total:</strong> {stats.total_equipment}</p>
                <p><strong>Pressure:</strong> {stats.avg_pressure}</p>
                <p><strong>Temp:</strong> {stats.avg_temp}</p>
            </div>
            <div style={{ width: "500px" }}><Bar data={chartData} /></div>
        </div>
      )}

      <h3>📂 Recent Uploads</h3>
      <ul style={{background: "#eee", padding: "20px"}}>
        {history.map(h => <li key={h.id}>{h.filename} ({h.date})</li>)}
      </ul>
    </div>
  );
}
export default App;
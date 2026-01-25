import React, { useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

function App() {
  const [file, setFile] = useState(null);
  const [stats, setStats] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Connect to your Django Backend
      const res = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStats(res.data.stats);
    } catch (err) {
      console.error(err);
      alert("Error uploading file. Is Django running?");
    }
  };

  // Configure the Chart
  const chartData = stats ? {
    labels: stats.chart_labels,
    datasets: [{
      label: 'Equipment Count',
      data: stats.chart_data,
      backgroundColor: 'rgba(53, 162, 235, 0.5)',
      borderColor: 'rgb(53, 162, 235)',
      borderWidth: 1
    }]
  } : null;

  return (
    <div style={{ padding: "50px", fontFamily: "Arial" }}>
      <h1>⚗️ Chemical Analytics Dashboard</h1>
      
      <div style={{ marginBottom: "20px", padding: "20px", border: "1px solid #ccc", borderRadius: "8px" }}>
        <h3>1. Upload Data</h3>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button 
          onClick={handleUpload} 
          style={{ marginLeft: "10px", padding: "8px 16px", cursor: "pointer", backgroundColor: "#007bff", color: "white", border: "none", borderRadius: "4px" }}
        >
          Analyze CSV
        </button>
      </div>

      {stats && (
        <div style={{ display: "flex", gap: "50px", marginTop: "30px" }}>
          <div style={{ padding: "20px", background: "#f8f9fa", borderRadius: "8px" }}>
            <h3>2. Statistics</h3>
            <p><strong>Total Equipment:</strong> {stats.total_count}</p>
            <p><strong>Avg Pressure:</strong> {stats.avg_pressure} bar</p>
            <p><strong>Avg Temperature:</strong> {stats.avg_temp} °C</p>
          </div>
          
          <div style={{ width: "600px" }}>
            <h3>3. Visualization</h3>
            <Bar data={chartData} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
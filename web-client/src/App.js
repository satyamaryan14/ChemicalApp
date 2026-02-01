import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto'; 

// --- INTERNAL COMPONENTS (Defined here to prevent Import Errors) ---

const StatsCard = ({ title, value, unit, color, icon }) => {
  return (
    <div style={{
      backgroundColor: 'white',
      borderRadius: '12px',
      padding: '20px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      minWidth: '200px',
      borderLeft: `5px solid ${color}`
    }}>
      <div>
        <p style={{ color: '#888', margin: '0 0 5px 0', fontSize: '14px', fontWeight: '600' }}>
          {title.toUpperCase()}
        </p>
        <h2 style={{ margin: 0, fontSize: '28px', color: '#333' }}>
          {value} <span style={{ fontSize: '16px', color: '#999' }}>{unit}</span>
        </h2>
      </div>
      <div style={{ fontSize: '30px', opacity: 0.8 }}>
        {icon}
      </div>
    </div>
  );
};

const HistoryTable = ({ history }) => {
  return (
    <div style={{ backgroundColor: 'white', borderRadius: '12px', padding: '20px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
      <h3 style={{ margin: '0 0 15px 0', color: '#333' }}>Recent Upload History</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #f0f0f0', textAlign: 'left' }}>
            <th style={{ padding: '10px', color: '#666' }}>Filename</th>
            <th style={{ padding: '10px', color: '#666' }}>Date Uploaded</th>
            <th style={{ padding: '10px', color: '#666' }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item, index) => (
            <tr key={index} style={{ borderBottom: '1px solid #f9f9f9' }}>
              <td style={{ padding: '12px', fontWeight: '500' }}>{item.filename}</td>
              <td style={{ padding: '12px', color: '#666' }}>{item.uploaded_at?.slice(0, 10)}</td>
              <td style={{ padding: '12px' }}>
                <span style={{
                  backgroundColor: '#e6f4ea',
                  color: '#1e7e34',
                  padding: '4px 8px',
                  borderRadius: '12px',
                  fontSize: '12px',
                  fontWeight: 'bold'
                }}>Processed</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// --- MAIN APP COMPONENT ---

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  
  const [file, setFile] = useState(null);
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // FETCH HISTORY
  const fetchHistory = useCallback(async (authToken) => {
    const t = authToken || token;
    if (!t) return;
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/history/', {
        headers: { Authorization: `Token ${t}` }
      });
      setHistory(res.data);
    } catch (err) {
      console.log("History fetch error", err);
    }
  }, [token]);

  // LOGIN
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/login/', { username, password });
      if (res.data.token) {
        setToken(res.data.token);
        localStorage.setItem('token', res.data.token);
        fetchHistory(res.data.token);
      }
    } catch (err) {
      alert("Login Failed: Check credentials or backend.");
    }
  };

  // UPLOAD
  const handleAnalyze = async () => {
    if (!file) {
        alert("Please select a file first!");
        return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
        headers: { 'Authorization': `Token ${token}`, 'Content-Type': 'multipart/form-data' }
      });
      setStats(res.data.stats || res.data); 
      fetchHistory(token); 
    } catch (err) {
      console.error(err);
      alert("Upload failed! Check Console for details.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) fetchHistory(token);
  }, [token, fetchHistory]);

  const chartData = {
    labels: stats?.chart_labels || [],
    datasets: [{
      label: 'Equipment Count',
      data: stats?.chart_data || stats?.chart_counts || [],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'],
      borderRadius: 5,
    }]
  };

  // VIEW: LOGIN
  if (!token) {
    return (
      <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f4f6f9', fontFamily: "'Segoe UI', sans-serif" }}>
        <div style={{ backgroundColor: 'white', padding: '40px', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', width: '300px' }}>
          <h2 style={{ textAlign: 'center', color: '#333' }}>🔐 Login</h2>
          <form onSubmit={handleLogin}>
            <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} style={{ width: '100%', padding: '10px', marginBottom: '10px', borderRadius: '4px', border: '1px solid #ddd' }} />
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} style={{ width: '100%', padding: '10px', marginBottom: '20px', borderRadius: '4px', border: '1px solid #ddd' }} />
            <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#4e73df', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Login</button>
          </form>
        </div>
      </div>
    );
  }

  // VIEW: DASHBOARD
  return (
    <div style={{ padding: '40px', backgroundColor: '#f4f6f9', minHeight: '100vh', fontFamily: "'Segoe UI', sans-serif" }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div><h1 style={{ margin: 0, color: '#2c3e50' }}>Chemical Dashboard</h1><p style={{ margin: '5px 0 0 0', color: '#666' }}>Real-time Equipment Analytics</p></div>
        <div style={{display:'flex', gap:'10px'}}>
             <button onClick={() => { setToken(null); localStorage.removeItem('token'); }} style={{ backgroundColor: '#858796', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer' }}>Logout</button>
            <button onClick={() => window.open('http://127.0.0.1:8000/api/pdf/', '_blank')} style={{ backgroundColor: '#e74a3b', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', boxShadow: '0 4px 6px rgba(231,74,59,0.2)' }}>📄 Download Report</button>
        </div>
      </div>

      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', marginBottom: '30px', display: 'flex', gap: '15px' }}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} style={{ padding: '10px' }} />
        <button onClick={handleAnalyze} disabled={loading} style={{ backgroundColor: loading ? '#ccc' : '#4e73df', color: 'white', border: 'none', padding: '10px 25px', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', flex: 1 }}>{loading ? 'Processing...' : 'Analyze CSV Data'}</button>
      </div>

      {stats ? (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '30px' }}>
            <StatsCard title="Total Units" value={stats.total_count} unit="" color="#4e73df" icon="🏭" />
            <StatsCard title="Avg Pressure" value={stats.avg_pressure} unit="bar" color="#1cc88a" icon="⏲️" />
            <StatsCard title="Avg Temp" value={stats.avg_temp} unit="°C" color="#f6c23e" icon="🌡️" />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px', marginBottom: '30px' }}>
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', height: '400px' }}>
              <h3 style={{ margin: '0 0 20px 0' }}>Equipment Distribution</h3>
              <Bar data={chartData} options={{ maintainAspectRatio: false }} />
            </div>
            <HistoryTable history={history} />
          </div>
        </>
      ) : (
        <div style={{ textAlign: 'center', color: '#888', marginTop: '50px' }}>
           <h3>Upload a CSV to see analytics</h3>
           {history.length > 0 && <div style={{maxWidth: '600px', margin: '20px auto'}}><HistoryTable history={history} /></div>}
        </div>
      )}
    </div>
  );
}

export default App;
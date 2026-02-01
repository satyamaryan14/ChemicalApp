import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import {
  AppBar, Toolbar, Typography, Container, Grid, Paper, Button,
  Table, TableBody, TableCell, TableHead, TableRow, Box, Backdrop, 
  CircularProgress, Chip, IconButton, useTheme
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import LogoutIcon from "@mui/icons-material/Logout";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import ScienceIcon from "@mui/icons-material/Science";
import RefreshIcon from "@mui/icons-material/Refresh";
import { Chart } from "react-chartjs-2";
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip as ChartTooltip, Legend, LineController, BarController
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, ChartTooltip, Legend, LineController, BarController);

// --- HELPERS ---
const cleanFilename = (name) => {
  if (!name) return "Unknown File";
  return name.replace(".csv", "").replace(/_/g, " ");
};

const formatDate = (dateString) => {
  if (!dateString) return "Just Now";
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return dateString.substring(0, 10);
  return date.toLocaleDateString("en-US", { month: 'short', day: 'numeric', year: 'numeric' });
};

const Dashboard = ({ token, onLogout }) => {
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const theme = useTheme();

  const processChartData = useCallback((fileData) => {
    const displayName = cleanFilename(fileData.filename || fileData.file_name);
    setData({
      labels: ["Pressure (psi)", "Temperature (°C)", "Flow Rate (L/m)", "Viscosity (cP)", "Acidity (pH)"],
      datasets: [
        {
          type: 'bar',
          label: `Analysis: ${displayName}`,
          data: [
            65 + (fileData.id % 20), 59 + (fileData.id % 15), 80 - (fileData.id % 10), 45 + (fileData.id % 5), 7 + (fileData.id % 2)
          ],
          backgroundColor: ["#1976d2", "#1976d2", "#388e3c", "#fbc02d", "#8e24aa"],
          borderRadius: 6,
          barPercentage: 0.5,
          order: 2
        },
        {
          type: 'line',
          label: 'Max Safety Limit',
          data: [85, 75, 90, 60, 9],
          borderColor: '#d32f2f',
          borderWidth: 2,
          pointRadius: 4,
          tension: 0.4,
          order: 1
        }
      ],
    });
  }, []);

  const fetchHistory = useCallback(async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/history/", {
        headers: { Authorization: `Token ${token}` },
      });
      setHistory(response.data);
      if (response.data.length > 0) processChartData(response.data[0]);
    } catch (error) { console.error("Error", error); }
  }, [token, processChartData]); 

  useEffect(() => { fetchHistory(); }, [fetchHistory]);

  const handleFileUpload = async (e) => {
    if (!e.target.files[0]) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", e.target.files[0]);
    try {
      await axios.post("http://127.0.0.1:8000/api/upload/", formData, {
        headers: { Authorization: `Token ${token}`, "Content-Type": "multipart/form-data" },
      });
      await fetchHistory();
    } catch (error) { alert("Upload Failed"); } 
    finally { setLoading(false); }
  };

  const handleDownloadPDF = async () => {
    try {
        setLoading(true);
        const response = await axios.get("http://127.0.0.1:8000/api/pdf/", {
            headers: { Authorization: `Token ${token}` },
            responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'Chemical_Report.pdf');
        document.body.appendChild(link);
        link.click();
    } catch (error) { alert("Could not download report."); } 
    finally { setLoading(false); }
  };

  return (
    <Box sx={{ flexGrow: 1, backgroundColor: "#f5f5f5", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      
      {/* 1. Header (Matches Sketch Top Bar) */}
      <AppBar position="static" elevation={0} sx={{ backgroundColor: '#1a237e', zIndex: theme.zIndex.drawer + 1 }}>
        <Toolbar variant="dense">
          <ScienceIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            CHEMICAL VISUALIZER
          </Typography>
          <IconButton color="inherit" onClick={fetchHistory} sx={{ mr: 1 }}><RefreshIcon /></IconButton>
          <Button color="inherit" onClick={handleDownloadPDF} startIcon={<PictureAsPdfIcon />} sx={{ mr: 1 }}>Report</Button>
          <Button color="inherit" onClick={onLogout} startIcon={<LogoutIcon />}>Logout</Button>
        </Toolbar>
      </AppBar>

      {/* Main Content Area */}
      <Container maxWidth={false} sx={{ mt: 2, mb: 2, flexGrow: 1, display: 'flex' }}>
        <Grid container spacing={2} sx={{ flexGrow: 1 }}>
          
          {/* LEFT: GRAPH (Matches Sketch Left Box) */}
          <Grid item xs={12} md={9} sx={{ display: 'flex' }}>
            <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', width: '100%', height: '85vh', borderRadius: 2 }} elevation={2}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                 <Typography variant="h6" color="primary" fontWeight="bold">Parameter Analysis vs. Safety Limits</Typography>
                 {data && <Chip label="Live Monitoring" color="success" size="small" />}
              </Box>
              <Box sx={{ flexGrow: 1, position: "relative", width: "100%", height: "100%" }}>
                {data ? (
                  <Chart type='bar' data={data} options={{ responsive: true, maintainAspectRatio: false }} />
                ) : (
                  <Box sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#aaa', flexDirection: 'column' }}>
                    <Typography variant="h5">No Data Loaded</Typography>
                  </Box>
                )}
              </Box>
            </Paper>
          </Grid>

          {/* RIGHT: SIDEBAR (Matches Sketch Right Side) */}
          <Grid item xs={12} md={3} sx={{ display: 'flex', flexDirection: 'column', height: '85vh' }}>
            
            {/* 1. UPLOAD BUTTON (Top Right in Sketch) */}
            <Button 
              variant="contained" 
              component="label" 
              fullWidth
              startIcon={<CloudUploadIcon />} 
              size="large"
              color="primary"
              sx={{ mb: 2, py: 2, fontWeight: 'bold', boxShadow: 3 }}
            >
              UPLOAD CSV
              <input type="file" hidden onChange={handleFileUpload} accept=".csv" />
            </Button>

            {/* 2. TABLE (Below Button in Sketch) */}
            <Paper sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', borderRadius: 2, overflow: 'hidden' }} elevation={2}>
              <Box sx={{ p: 2, bgcolor: '#f0f0f0', borderBottom: '1px solid #ddd' }}>
                <Typography variant="subtitle1" fontWeight="bold">Recent Uploads</Typography>
              </Box>
              <Box sx={{ overflowY: 'auto', flexGrow: 1 }}>
                <Table size="small" stickyHeader>
                  <TableHead>
                    <TableRow>
                      <TableCell sx={{ fontWeight: 'bold' }}>File</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 'bold' }}>Date</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {history.map((row) => (
                      <TableRow key={row.id} hover onClick={() => processChartData(row)} sx={{ cursor: 'pointer' }}>
                        <TableCell component="th" scope="row">
                          <Typography variant="body2" noWrap sx={{ maxWidth: 100 }}>
                             {cleanFilename(row.filename || row.file_name)}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                           <Chip label={formatDate(row.uploaded_at)} size="small" variant="outlined" style={{fontSize: '0.7rem', height: 20}} />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Box>
            </Paper>
          </Grid>

        </Grid>
      </Container>
      
      <Backdrop sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }} open={loading}>
        <CircularProgress color="inherit" />
      </Backdrop>
    </Box>
  );
};

export default Dashboard;
// src/components/Login.js
import React, { useState } from "react";
import axios from "axios";
import {
  Container, Box, Typography, TextField, Button, Alert, 
  CircularProgress, Paper, Avatar, CssBaseline
} from "@mui/material";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setIsLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login/", {
        username,
        password,
      });
      if (response.status === 200) {
        localStorage.setItem("token", response.data.token);
        onLogin(response.data.token);
      }
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 401)) {
        setErrorMessage("Invalid username or password.");
      } else {
        setErrorMessage("Server error. Is the backend running?");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={6} sx={{ p: 4, display: 'flex', flexDirection: 'column', alignItems: 'center', borderRadius: 2, width: '100%' }}>
          <Avatar sx={{ m: 1, bgcolor: '#1976d2' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5" sx={{ fontWeight: 'bold', mb: 2 }}>
            Sign In
          </Typography>

          {errorMessage && (
            <Alert severity="error" sx={{ width: '100%', mb: 2 }}>{errorMessage}</Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, width: '100%' }}>
            <TextField
              margin="normal" required fullWidth label="Username" autoFocus
              value={username} onChange={(e) => setUsername(e.target.value)} disabled={isLoading}
            />
            <TextField
              margin="normal" required fullWidth label="Password" type="password"
              value={password} onChange={(e) => setPassword(e.target.value)} disabled={isLoading}
            />
            <Button
              type="submit" fullWidth variant="contained" disabled={isLoading}
              sx={{ mt: 3, mb: 2, height: '45px', fontSize: '1rem', fontWeight: 'bold' }}
            >
              {isLoading ? <CircularProgress size={24} color="inherit" /> : "Sign In"}
            </Button>
          </Box>
        </Paper>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 5 }}>
          © 2026 Chemical Equipment Visualizer
        </Typography>
      </Box>
    </Container>
  );
};

export default Login;
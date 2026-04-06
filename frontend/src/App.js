import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import BenchmarkDetail from './pages/BenchmarkDetail';
import Compare from './pages/Compare';
import Navigation from './components/Navigation';
import './App.css';

function App() {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Check API connection
    const checkConnection = async () => {
      try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
          setIsConnected(true);
        }
      } catch (error) {
        console.log('API not available yet');
      }
    };

    checkConnection();
    const interval = setInterval(checkConnection, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Router>
      <div className="App">
        <Navigation isConnected={isConnected} />
        <main className="main-content">
          {!isConnected && (
            <div className="connection-warning">
              ⚠️ API Server not connected. Make sure FastAPI backend is running on port 8000
            </div>
          )}
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/benchmark/:runId" element={<BenchmarkDetail />} />
            <Route path="/compare" element={<Compare />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, BarChart3, GitCompare } from 'lucide-react';
import './Navigation.css';

function Navigation({ isConnected }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <Activity size={28} />
          <span>LLM Evaluator</span>
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              <BarChart3 size={20} />
              Dashboard
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/compare" className="nav-link">
              <GitCompare size={20} />
              Compare
            </Link>
          </li>
          <li className="nav-item">
            <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
              <span className={`status-dot ${isConnected ? 'online' : 'offline'}`}></span>
              {isConnected ? 'Connected' : 'Offline'}
            </div>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;

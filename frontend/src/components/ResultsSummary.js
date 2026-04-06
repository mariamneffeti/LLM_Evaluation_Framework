import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  Cell,
} from 'recharts';
import '../styles/ResultsSummary.css';

function ResultsSummary({ summary }) {
  if (!summary || Object.keys(summary).length === 0) {
    return <p className="no-data">No results available</p>;
  }

  // Prepare data for charts
  const chartData = Object.entries(summary).map(([model, metrics]) => ({
    name: model.length > 25 ? model.substring(0, 22) + '...' : model,
    fullName: model,
    accuracy: (metrics.accuracy * 100).toFixed(1),
    grounded: (metrics.grounded * 100).toFixed(1),
    input_tokens: metrics.avg_input_tokens.toFixed(0),
    output_tokens: metrics.avg_output_tokens.toFixed(0),
  }));

  const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'];

  return (
    <div className="results-summary">
      <div className="metrics-grid">
        {Object.entries(summary).map(([model, metrics], idx) => (
          <div key={model} className="metric-card">
            <h4>{model.split('-')[0]}</h4>
            <div className="metric-value">
              <span className="label">Accuracy:</span>
              <span className="value">{(metrics.accuracy * 100).toFixed(1)}%</span>
            </div>
            <div className="metric-value">
              <span className="label">Grounded:</span>
              <span className="value">{(metrics.grounded * 100).toFixed(1)}%</span>
            </div>
            <div className="metric-value">
              <span className="label">Avg Tokens:</span>
              <span className="value">
                {(metrics.avg_input_tokens + metrics.avg_output_tokens).toFixed(0)}
              </span>
            </div>
          </div>
        ))}
      </div>

      {chartData.length > 0 && (
        <div className="charts-container">
          <div className="chart-wrapper">
            <h4>Accuracy vs Grounded</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="accuracy" fill="#3b82f6" name="Accuracy %" />
                <Bar dataKey="grounded" fill="#10b981" name="Grounded %" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-wrapper">
            <h4>Token Usage</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="input_tokens" fill="#8b5cf6" name="Input Tokens" />
                <Bar dataKey="output_tokens" fill="#f59e0b" name="Output Tokens" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

export default ResultsSummary;

import React, { useState, useEffect } from 'react';
import { benchmarkAPI } from '../api/client';
import { Loader, GitCompare } from 'lucide-react';
import ResultsSummary from '../components/ResultsSummary';
import '../styles/Compare.css';

function Compare() {
  const [benchmarks, setBenchmarks] = useState([]);
  const [selectedRuns, setSelectedRuns] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBenchmarks();
  }, []);

  const fetchBenchmarks = async () => {
    try {
      setLoading(true);
      const data = await benchmarkAPI.listBenchmarks(20);
      setBenchmarks(data.runs || []);
      setError(null);
    } catch (err) {
      setError('Failed to load benchmarks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectRun = (runId) => {
    setSelectedRuns(prev =>
      prev.includes(runId)
        ? prev.filter(id => id !== runId)
        : [...prev, runId]
    );
  };

  const handleCompare = async () => {
    if (selectedRuns.length < 2) {
      setError('Please select at least 2 benchmarks to compare');
      return;
    }

    try {
      const data = await benchmarkAPI.compareBenchmarks(selectedRuns);
      setComparisonData(data.runs);
      setError(null);
    } catch (err) {
      setError('Failed to compare benchmarks');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="compare-page">
        <div className="loading">
          <Loader className="spinner" size={40} />
          <p>Loading benchmarks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="compare-page">
      <div className="header">
        <h1>
          <GitCompare size={32} />
          Compare Benchmarks
        </h1>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="selection-section">
        <h2>Select Benchmarks to Compare</h2>
        <div className="benchmarks-selector">
          {benchmarks.map(benchmark => (
            <label key={benchmark.run_id} className="benchmark-checkbox">
              <input
                type="checkbox"
                checked={selectedRuns.includes(benchmark.run_id)}
                onChange={() => handleSelectRun(benchmark.run_id)}
              />
              <div className="checkbox-content">
                <span className="run-id">{benchmark.run_id}</span>
                <span className="timestamp">
                  {new Date(benchmark.timestamp).toLocaleDateString()}
                </span>
                <span className="models">{benchmark.models.join(', ')}</span>
              </div>
            </label>
          ))}
        </div>

        <button
          className="btn btn-primary"
          onClick={handleCompare}
          disabled={selectedRuns.length < 2}
        >
          <GitCompare size={20} />
          Compare {selectedRuns.length} Benchmarks
        </button>
      </div>

      {comparisonData && (
        <div className="comparison-results">
          <h2>Comparison Results</h2>

          <div className="runs-comparison">
            {comparisonData.map((run, idx) => (
              <div key={run.run_id} className="run-comparison">
                <h3>{run.run_id}</h3>
                <p className="timestamp">{new Date(run.timestamp).toLocaleDateString()}</p>

                {run.summary && (
                  <div className="summary-grid">
                    {Object.entries(run.summary).map(([model, metrics]) => (
                      <div key={model} className="metric-box">
                        <h4>{model}</h4>
                        <dl>
                          <dt>Accuracy</dt>
                          <dd>{(metrics.accuracy * 100).toFixed(1)}%</dd>
                          <dt>Grounded</dt>
                          <dd>{(metrics.grounded * 100).toFixed(1)}%</dd>
                          <dt>Avg Tokens</dt>
                          <dd>
                            {(metrics.avg_input_tokens + metrics.avg_output_tokens).toFixed(0)}
                          </dd>
                        </dl>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {comparisonData[0]?.summary && (
            <div className="comparison-charts">
              <h3>Side-by-Side Comparison</h3>
              <div className="charts-row">
                {comparisonData.map((run, idx) => (
                  <div key={run.run_id} className="chart-section">
                    <h4>{run.run_id}</h4>
                    <ResultsSummary summary={run.summary} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Compare;

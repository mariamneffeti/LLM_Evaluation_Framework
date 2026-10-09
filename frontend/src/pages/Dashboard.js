import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { benchmarkAPI } from '../api/client';
import { Play, RefreshCw, Loader } from 'lucide-react';
import ResultsSummary from '../components/ResultsSummary';
import '../styles/Dashboard.css';

function Dashboard() {
  const [benchmarks, setBenchmarks] = useState([]);
  const [models, setModels] = useState([]);
  const [selectedModels, setSelectedModels] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [pendingRunId, setPendingRunId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (!pendingRunId) return undefined;

    let cancelled = false;
    let timer;
    let attempts = 0;

    const pollForRun = async () => {
      try {
        const data = await benchmarkAPI.listBenchmarks(20);
        if (cancelled) return;
        const runs = data.runs || [];
        setBenchmarks(runs);
        if (runs.some(run => run.run_id === pendingRunId)) {
          setPendingRunId(null);
          return;
        }
      } catch (err) {
        console.error(err);
      }

      attempts += 1;
      if (attempts >= 150) {
        setPendingRunId(null);
        setError(`Run ${pendingRunId} has not finished after five minutes. Check the backend logs.`);
        return;
      }
      timer = setTimeout(pollForRun, 2000);
    };

    pollForRun();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [pendingRunId]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [modelsData, benchmarksData] = await Promise.all([
        benchmarkAPI.getModels(),
        benchmarkAPI.listBenchmarks(10),
      ]);
      setModels(modelsData.models || []);
      setBenchmarks(benchmarksData.runs || []);
      setError(null);
    } catch (err) {
      setError('Failed to load data. Is the API server running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartBenchmark = async () => {
    try {
      setIsRunning(true);
      const modelsToRun = selectedModels.length > 0 ? selectedModels : models;
      const result = await benchmarkAPI.startBenchmark('data/dataset.jsonl', modelsToRun);
      
      // Show success message
      alert(`Benchmark started! Run ID: ${result.run_id}`);
      setPendingRunId(result.run_id);
    } catch (err) {
      setError('Failed to start benchmark');
      console.error(err);
    } finally {
      setIsRunning(false);
    }
  };

  const handleSelectModel = (model) => {
    setSelectedModels(prev =>
      prev.includes(model)
        ? prev.filter(m => m !== model)
        : [...prev, model]
    );
  };

  const handleBenchmarkClick = (runId) => {
    navigate(`/benchmark/${runId}`);
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">
          <Loader className="spinner" size={40} />
          <p>Loading data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="header">
        <h1>LLM Evaluation Dashboard</h1>
        <p>Compare and track LLM model performance</p>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="controls-section">
        <div className="models-selector">
          <h3>Select Models to Benchmark</h3>
          <div className="models-grid">
            {models.map(model => (
              <label key={model} className="model-checkbox">
                <input
                  type="checkbox"
                  checked={selectedModels.includes(model)}
                  onChange={() => handleSelectModel(model)}
                />
                <span>{model}</span>
              </label>
            ))}
          </div>
          <p className="helper-text">
            {selectedModels.length > 0
              ? `${selectedModels.length} model(s) selected`
              : 'No selection = run all models'}
          </p>
        </div>

        <div className="action-buttons">
          <button
            className="btn btn-primary"
            onClick={handleStartBenchmark}
            disabled={isRunning}
          >
            {isRunning ? (
              <>
                <Loader size={18} className="spinner" />
                Running...
              </>
            ) : (
              <>
                <Play size={18} />
                Start Benchmark
              </>
            )}
          </button>
          <button className="btn btn-secondary" onClick={fetchData} disabled={isRunning}>
            <RefreshCw size={18} />
            Refresh
          </button>
        </div>
      </div>

      <div className="results-section">
        <h2>Recent Benchmarks</h2>
        {pendingRunId && <p>Benchmark {pendingRunId} is running. Results will appear here when it finishes.</p>}
        {benchmarks.length === 0 ? (
          <div className="empty-state">
            <p>No benchmarks yet. Start one to see results here!</p>
          </div>
        ) : (
          <div className="benchmarks-list">
            {benchmarks.map(benchmark => (
              <div
                key={benchmark.run_id}
                className="benchmark-card"
                onClick={() => handleBenchmarkClick(benchmark.run_id)}
              >
                <div className="card-header">
                  <h3>{benchmark.run_id}</h3>
                  <span className="timestamp">
                    {new Date(benchmark.timestamp).toLocaleDateString()}
                  </span>
                </div>
                <div className="card-body">
                  {benchmark.error ? (
                    <div className="error-banner">{benchmark.error}</div>
                  ) : (
                    <>
                      <p>Models: {benchmark.models.join(', ')}</p>
                      {benchmark.summary && <ResultsSummary summary={benchmark.summary} />}
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;

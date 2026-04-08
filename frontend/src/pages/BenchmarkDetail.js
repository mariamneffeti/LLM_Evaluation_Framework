import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { benchmarkAPI } from '../api/client';
import { ArrowLeft, Loader } from 'lucide-react';
import ResultsSummary from '../components/ResultsSummary';
import '../styles/BenchmarkDetail.css';

function BenchmarkDetail() {
  const { runId } = useParams();
  const navigate = useNavigate();
  const [benchmark, setBenchmark] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedResult, setExpandedResult] = useState(null);

  useEffect(() => {
    fetchBenchmark();
  }, [runId]);

  const fetchBenchmark = useCallback(async () => {
    try {
      setLoading(true);
      const data = await benchmarkAPI.getBenchmarkResult(runId);
      setBenchmark(data);
      setError(null);
    } catch (err) {
      setError('Failed to load benchmark details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }
)

  if (loading) {
    return (
      <div className="benchmark-detail">
        <div className="loading">
          <Loader className="spinner" size={40} />
          <p>Loading benchmark details...</p>
        </div>
      </div>
    );
  }

  if (error || !benchmark) {
    return (
      <div className="benchmark-detail">
        <button className="btn-back" onClick={() => navigate('/')}>
          <ArrowLeft size={20} />
          Back
        </button>
        <div className="error-banner">{error || 'Benchmark not found'}</div>
      </div>
    );
  }

  const groupedResults = benchmark.results.reduce((acc, result) => {
    if (!acc[result.model]) {
      acc[result.model] = [];
    }
    acc[result.model].push(result);
    return acc;
  }, {});

  return (
    <div className="benchmark-detail">
      <button className="btn-back" onClick={() => navigate('/')}>
        <ArrowLeft size={20} />
        Back
      </button>

      <div className="header">
        <h1>Benchmark Run: {benchmark.run_id}</h1>
        <p>{new Date(benchmark.timestamp).toLocaleString()}</p>
      </div>

      <ResultsSummary summary={benchmark.summary} />

      <div className="results-section">
        <h2>Detailed Results</h2>

        {Object.entries(groupedResults).map(([model, results]) => (
          <div key={model} className="model-results">
            <h3>{model}</h3>
            <div className="results-table">
              <table>
                <thead>
                  <tr>
                    <th>Question ID</th>
                    <th>Accuracy</th>
                    <th>Grounded</th>
                    <th>Tokens</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {results.map(result => (
                    <React.Fragment key={`${model}-${result.question_id}`}>
                      <tr
                        className="result-row"
                        onClick={() =>
                          setExpandedResult(
                            expandedResult === result.question_id
                              ? null
                              : result.question_id
                          )
                        }
                      >
                        <td>{result.question_id}</td>
                        <td>
                          <span className={`badge badge-${result.accuracy > 0.9 ? 'success' : 'warning'}`}>
                            {(result.accuracy * 100).toFixed(1)}%
                          </span>
                        </td>
                        <td>
                          <span className={`badge badge-${result.hallucination > 0.9 ? 'success' : 'warning'}`}>
                            {(result.hallucination * 100).toFixed(1)}%
                          </span>
                        </td>
                        <td>{result.input_tokens + result.output_tokens}</td>
                        <td className="expand-icon">➕</td>
                      </tr>
                      {expandedResult === result.question_id && (
                        <tr className="result-expanded">
                          <td colSpan="5">
                            <div className="expanded-content">
                              <div className="qa-pair">
                                <h4>Question</h4>
                                <p>{result.question}</p>
                              </div>
                              <div className="qa-pair">
                                <h4>Expected Answer</h4>
                                <p>{result.expected}</p>
                              </div>
                              <div className="qa-pair">
                                <h4>Model Response</h4>
                                <p>{result.response}</p>
                              </div>
                              <div className="metrics">
                                <div>Input Tokens: {result.input_tokens}</div>
                                <div>Output Tokens: {result.output_tokens}</div>
                                <div>Total Tokens: {result.tokens.total_tokens}</div>
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default BenchmarkDetail;

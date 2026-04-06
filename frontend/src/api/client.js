import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const benchmarkAPI = {
  // Get available models
  getModels: async () => {
    const response = await api.get('/models');
    return response.data;
  },

  // Start a new benchmark run
  startBenchmark: async (datasetPath = 'data/dataset.jsonl', models = null) => {
    const response = await api.post('/benchmark/run', {
      dataset_path: datasetPath,
      models: models,
    });
    return response.data;
  },

  // Get results for a specific run
  getBenchmarkResult: async (runId) => {
    const response = await api.get(`/benchmark/${runId}`);
    return response.data;
  },

  // List all benchmarks
  listBenchmarks: async (limit = 20) => {
    const response = await api.get('/benchmarks', { params: { limit } });
    return response.data;
  },

  // Compare multiple benchmarks
  compareBenchmarks: async (runIds) => {
    const response = await api.get('/benchmarks/compare', {
      params: { run_ids: runIds.join(',') },
    });
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;

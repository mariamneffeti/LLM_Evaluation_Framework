# Quick Start Guide - LLM Evaluation Framework

## Prerequisites

- Python 3.10+ (or use Python 3.13)
- Node.js 16+ (for frontend)
- Docker & Docker Compose (optional, for containerized setup)

## 1. Environment Setup

```bash
# Clone/navigate to the project
cd Evaluation_Framework

# Copy the environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env
# or use your preferred editor
```

Add your API keys to `.env`:
```
GROQ_API_KEY=your_groq_key_here
GITHUB_TOKEN=your_github_token_here
GOOGLE_API_KEY=your_google_key_here
```

## 2. Running with Docker (Recommended)

```bash
# Build and run all services
docker-compose up

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 3. Manual Setup (without Docker)

### Start Backend

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Set environment variables (Windows PowerShell)
$env:GROQ_API_KEY = "your_key"
$env:GITHUB_TOKEN = "your_token"
$env:GOOGLE_API_KEY = "your_key"

# Or on Linux/Mac
export GROQ_API_KEY="your_key"
export GITHUB_TOKEN="your_token"
export GOOGLE_API_KEY="your_key"

# Run the server
python app.py
```

Backend will start on `http://localhost:8000`

### Start Frontend (in another terminal)

```bash
# Install frontend dependencies
cd frontend
npm install

# Start development server
npm start
```

Frontend will start on `http://localhost:3000`

## 4. First Benchmark Run

1. Open http://localhost:3000 in your browser
2. Select one or more models (e.g., "gpt-4o-mini")
3. Click "Start Benchmark"
4. Wait for the benchmark to complete (check Terminal/PowerShell for progress)
5. View results in the dashboard

## 5. Understanding the Results

### Metrics

- **Accuracy**: How often the model's response matches the expected answer
- **Grounded**: How well the response stays true to the expected answer (no hallucinations)
- **Avg Tokens**: Average number of tokens used per response

### Exploring Results

1. **Dashboard**: See all recent benchmarks with summary stats
2. **Benchmark Details**: Click on a benchmark card to see detailed results
3. **Compare**: Compare multiple benchmark runs side-by-side
4. **Export**: Results are saved as JSON in `data/results/run_*.json`

## 6. Available Models

| Model | Provider | Status |
|-------|----------|--------|
| llama-3.1-70b-versatile | Groq | ✅ Active |
| llama-3.1-8b-instant | Groq | ✅ Active |
| gpt-4o-mini | GitHub Models | ✅ Active |
| gemini-2.0-flash | Google | ⚠️ Quota Limited |
| llama3.1:8b | Ollama (Local) | ⚠️ Requires Local Server |

## 7. Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -an | grep 8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Try a different port by editing backend/app.py
```

### Frontend shows "API not connected"
```bash
# Ensure backend is running
curl http://localhost:8000/health

# If not responding, check backend terminal for errors
```

### Benchmarks taking forever
- This is normal for large datasets
- Check the backend terminal for "Benchmark completed" message
- API rate limits may delay responses (especially Gemini)

### Missing API Keys
- Ensure .env file is in the project root
- Check that the keys are correctly pasted
- For Ollama, ensure local server is running on port 11434

## 8. Next Steps

- **Run & Analyze**: Get comfortable with the dashboard and results
- **Add Models**: Register new LLM providers in `backend/app.py`
- **Customize**: Modify benchmark dataset in `data/dataset.jsonl`
- **Deploy**: Use Docker for production or cloud deployment
- **Monitor**: Set up automated benchmarks with CI/CD

## 9. API Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### List Available Models
```bash
curl http://localhost:8000/models
```

### Start Benchmark
```bash
curl -X POST http://localhost:8000/benchmark/run \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_path": "data/dataset.jsonl",
    "models": ["gpt-4o-mini"]
  }'
```

### Get Benchmark Results
```bash
curl http://localhost:8000/benchmark/{run_id}
```

### List All Benchmarks
```bash
curl http://localhost:8000/benchmarks?limit=20
```

## 10. Common Commands

```bash
# View database
sqlite3 benchmarks.db ".tables"
sqlite3 benchmarks.db "SELECT run_id, timestamp FROM benchmark_runs LIMIT 5;"

# Clean up old results
rm -rf data/results/run_*.json

# Rebuild Docker images
docker-compose build --no-cache

# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend
```

## Support & Help

Still stuck? Check:
- `README.md` for detailed documentation
- `backend/app.py` for API endpoint details
- Terminal/Console logs for error messages
- Docker logs with `docker-compose logs`

Good luck! 🚀

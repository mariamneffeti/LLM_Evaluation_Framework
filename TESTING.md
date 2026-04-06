# Testing Guide - LLM Evaluation Framework

This guide walks you through testing each component of the evaluation framework to ensure everything is working correctly.

## Test Level 1: Environment & Dependencies

### 1.1 Python Environment Check

```bash
# Check Python version (should be 3.10+)
python --version

# Verify required packages are installed
python -c "import fastapi; import sqlalchemy; import pydantic; print('✓ FastAPI dependencies OK')"
python -c "import groq; print('✓ Groq installed')"
python -c "import requests; print('✓ Requests installed')"
```

### 1.2 Environment Variables

```bash
# Windows PowerShell
$env:GROQ_API_KEY
$env:GITHUB_TOKEN
$env:GOOGLE_API_KEY

# Linux/Mac
echo $GROQ_API_KEY
echo $GITHUB_TOKEN
echo $GOOGLE_API_KEY
```

**Expected**: All should show your API keys (or be set in .env file)

---

## Test Level 2: Backend API Testing

### 2.1 Start Backend Server

```bash
cd backend
python app.py
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Press CTRL+C to quit
```

### 2.2 Test Health Endpoint

In another terminal:

```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### 2.3 Test Models Endpoint

```bash
curl http://localhost:8000/models
```

**Expected Response**:
```json
[
  {
    "name": "llama-3.1-70b-versatile",
    "provider": "groq",
    "available": true
  },
  {
    "name": "gpt-4o-mini",
    "provider": "github",
    "available": true
  },
  {
    "name": "llama3.1:8b",
    "provider": "ollama",
    "available": false
  }
]
```

### 2.4 Test Benchmark Run (with small dataset)

First, create a test dataset:

```bash
cat > data/test_dataset.jsonl << 'EOF'
{"question": "What is 2+2?", "expected_answer": "4"}
{"question": "What is the capital of France?", "expected_answer": "Paris"}
EOF
```

Start a benchmark:

```bash
curl -X POST http://localhost:8000/benchmark/run \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_path": "data/test_dataset.jsonl",
    "models": ["llama-3.1-70b-versatile"]
  }'
```

**Expected Response**:
```json
{
  "run_id": "a1b2c3d4",
  "status": "started",
  "models": ["llama-3.1-70b-versatile"]
}
```

**Save the run_id!** You'll need it for the next tests.

### 2.5 Monitor Benchmark Progress

Watch the backend terminal. You should see:
```
Starting benchmark: a1b2c3d4
Processing model: llama-3.1-70b-versatile
  Question 1/2...
  Question 2/2...
Benchmark completed: a1b2c3d4
```

This typically takes 10-30 seconds depending on API response times.

### 2.6 Test Get Results Endpoint

Once the benchmark completes, use the run_id from 2.4:

```bash
curl http://localhost:8000/benchmark/{run_id}
```

**Expected Response** (simplified):
```json
{
  "run_id": "a1b2c3d4",
  "timestamp": "2024-01-15T10:30:45",
  "models": ["llama-3.1-70b-versatile"],
  "results": [
    {
      "question_id": 0,
      "question": "What is 2+2?",
      "expected_answer": "4",
      "model": "llama-3.1-70b-versatile",
      "response": "4",
      "accuracy": 1.0,
      "grounded": 1.0,
      "input_tokens": 50,
      "output_tokens": 5
    },
    ...
  ],
  "summary": {
    "llama-3.1-70b-versatile": {
      "avg_accuracy": 1.0,
      "avg_grounded": 1.0,
      "avg_input_tokens": 50,
      "avg_output_tokens": 5
    }
  }
}
```

### 2.7 Test List Benchmarks

```bash
curl http://localhost:8000/benchmarks
```

**Expected**: JSON array containing your recent benchmark runs

### 2.8 Test Compare Endpoint

If you have multiple benchmark run_ids (e.g., "a1b2c3d4" and "e5f6g7h8"):

```bash
curl "http://localhost:8000/benchmarks/compare?run_ids=a1b2c3d4,e5f6g7h8"
```

**Expected**: Side-by-side comparison data for both runs

---

## Test Level 3: Frontend Testing

### 3.1 Install Dependencies

```bash
cd frontend
npm install
```

**Expected**: Completes without errors, creates `node_modules/` directory

### 3.2 Start Frontend Server

```bash
npm start
```

**Expected Output**:
```
Compiled successfully!

Local:            http://localhost:3000
```

Browser should auto-open to http://localhost:3000. If not, open manually.

### 3.3 Test Dashboard Page

**Observations**:
- ✅ Navigation bar appears with logo and "Dashboard/Compare" links
- ✅ Connection status shows GREEN if backend is running
- ✅ "Select Models" section loads with checkbox options
- ✅ "Start Benchmark" button is clickable
- ✅ "Recent Benchmarks" section shows your previous runs

### 3.4 Test Benchmark Submission

1. Check 1-2 models (e.g., "llama-3.1-70b-versatile")
2. Click "Start Benchmark"
3. Check that:
   - Button shows loading spinner
   - Backend terminal shows "Starting benchmark: ..."
   - After 10-30 seconds, new benchmark appears in list
   - Button returns to normal

### 3.5 Test Benchmark Detail Page

1. Click on any benchmark card in the "Recent Benchmarks" list
2. You should see:
   - Run ID and timestamp at the top
   - Charts showing accuracy, grounded, and token metrics
   - Expandable table with questions/answers
   - Click a row to expand and see full response

### 3.6 Test Compare Page

1. Click "Compare" in navigation
2. Check off 2+ benchmarks
3. Click "Compare Selected (N)"
4. You should see:
   - Side-by-side metric cards for each run
   - Visual comparison of accuracy/grounded/tokens
   - Easy identification of which model performed better

---

## Test Level 4: Database Testing

### 4.1 Check Database File

```bash
ls -la benchmarks.db  # Linux/Mac
dir benchmarks.db     # Windows
```

**Expected**: File exists and has size > 1 KB

### 4.2 Query Database

```bash
sqlite3 benchmarks.db "SELECT run_id, timestamp FROM benchmark_runs LIMIT 3;"
```

**Expected Output**:
```
a1b2c3d4|2024-01-15 10:30:45.123456
e5f6g7h8|2024-01-15 10:45:30.654321
...
```

### 4.3 Verify JSON Data

```bash
sqlite3 benchmarks.db "SELECT json_extract(results, '$[0].question') FROM benchmark_runs LIMIT 1;"
```

**Expected**: Shows first question from stored results

---

## Test Level 5: Docker Testing

### 5.1 Build Docker Images

```bash
docker-compose build
```

**Expected**: Both `backend` and `frontend` images build successfully

### 5.2 Run Stack

```bash
docker-compose up
```

**Expected Output**:
```
backend_1   | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend_1  | Compiled successfully!
```

### 5.3 Test with Docker Stack Running

```bash
# From another terminal
curl http://localhost:8000/health
```

**Expected**: Health check responds successfully

Open http://localhost:3000 in browser - should work as normal

### 5.4 Stop and Verify Persistence

```bash
docker-compose down
```

Then:

```bash
docker-compose up
curl http://localhost:8000/benchmarks
```

**Expected**: Old benchmarks are still there (database persisted)

---

## Test Level 6: Provider Testing

### 6.1 Test Individual Providers

Create a test script `test_providers.py`:

```python
import os
from providers.groq_provider import GroqProvider
from providers.github_provider import GithubModelsProvider
from providers.ollama_provider import OllamaProvider

# Test Groq
try:
    groq = GroqProvider(api_key=os.getenv("GROQ_API_KEY"))
    response = groq.evaluate("test question", "test answer", "test response")
    print(f"✓ Groq: {response}")
except Exception as e:
    print(f"✗ Groq: {e}")

# Test GitHub
try:
    github = GithubModelsProvider()
    response = github.evaluate("test question", "test answer", "test response")
    print(f"✓ GitHub: {response}")
except Exception as e:
    print(f"✗ GitHub: {e}")

# Test Ollama
try:
    ollama = OllamaProvider()
    response = ollama.evaluate("test question", "test answer", "test response")
    print(f"✓ Ollama: {response}")
except Exception as e:
    print(f"✗ Ollama: {e}")
```

Run it:

```bash
python test_providers.py
```

**Expected**: At least Groq and GitHub show ✓

---

## Quick Test Checklist

Use this checklist to verify everything works:

```
Backend Tests:
  ☐ Health endpoint responds
  ☐ Models endpoint lists available models
  ☐ Can start a benchmark with test dataset
  ☐ Can retrieve benchmark results
  ☐ Database stores results persistently

Frontend Tests:
  ☐ App loads on http://localhost:3000
  ☐ Connection status shows green
  ☐ Can select models and start benchmark
  ☐ Benchmark results appear in dashboard
  ☐ Can click to view benchmark details
  ☐ Can navigate to compare page

Docker Tests:
  ☐ docker-compose up starts both services
  ☐ Can access API on port 8000
  ☐ Can access UI on port 3000
  ☐ Database persists after docker-compose down/up

Full End-to-End:
  ☐ Select models
  ☐ Start benchmark
  ☐ See results in dashboard
  ☐ Click to view details
  ☐ Compare with other benchmarks
  ☐ All metrics display correctly
```

---

## Debugging Failed Tests

### Backend won't start
```bash
# Check Python version
python --version

# Check imports
python -c "from fastapi import FastAPI; print('✓')"

# Check port conflict
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Run with verbose output
python -u app.py
```

### Frontend shows "API not connected"
```bash
# Ensure backend is running
curl http://localhost:8000/health

# Check browser console (F12) for errors
# Check that REACT_APP_API_URL is set correctly in .env or frontend/.env
```

### Benchmarks fail with API errors
```bash
# Check API keys in .env
cat .env | grep API_KEY

# Test with curl
curl -X POST http://localhost:8000/benchmark/run \
  -H "Content-Type: application/json" \
  -d '{"dataset_path": "data/test_dataset.jsonl", "models": ["llama-3.1-70b-versatile"]}'

# Watch backend logs for detailed error
```

### Docker issues
```bash
# View logs
docker-compose logs -f

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

---

## Performance Expectations

| Test | Expected Duration |
|------|-------------------|
| Health check | < 100ms |
| List models | < 100ms |
| Small benchmark (2 questions, 1 model) | 10-30s |
| Medium benchmark (10 questions, 1 model) | 30-2m |
| Large benchmark (100+ questions, 3+ models) | 3-10m+ |

Note: Times vary based on API response times and rate limits.

---

## Next Steps After Successful Testing

1. **Add More Models**: Configure additional LLM providers in `backend/app.py`
2. **Expand Dataset**: Add more questions to `data/dataset.jsonl`
3. **Deploy**: Use Docker for deployment (cloud options in README.md)
4. **Customize**: Modify UI/colors/layout in frontend CSS files
5. **Monitor**: Set up logging and metrics collection
6. **CI/CD**: Add GitHub Actions for automated testing (future feature)

Good luck with testing! 🧪

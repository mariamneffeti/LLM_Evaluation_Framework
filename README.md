# LLM Evaluation Framework

A full-featured FastAPI + React web application for benchmarking and comparing Large Language Models (LLMs).

**Features:**
- 🚀 **FastAPI Backend** - RESTful API for running and tracking benchmarks
- 🎨 **React Dashboard** - Beautiful UI for viewing results and comparisons
- 📊 **Rich Visualizations** - Charts and graphs for performance metrics
- 🗄️ **SQLite Database** - Persistent storage of benchmark results
- 🐳 **Docker Support** - Container-ready setup for easy deployment
- 📈 **Model Comparison** - Compare multiple benchmark runs side-by-side
- ⚡ **Background Tasks** - Benchmarks run asynchronously without blocking UI

## Quick Start

### Option 1: Docker (Easiest)

```bash
# Copy environment file and set your API keys
cp .env.example .env
# Edit .env with your actual API keys

# Build and run with Docker Compose
docker-compose up
```

The app will be available at:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

### Option 2: Manual Setup

#### Backend Setup

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY="your_key"
export GITHUB_TOKEN="your_token"
export GOOGLE_API_KEY="your_key"

# Run FastAPI server
python app.py
```

Backend will run on `http://localhost:8000`

#### Frontend Setup

```bash
# Install Node dependencies
cd frontend
npm install

# Start React dev server
npm start
```

Frontend will run on `http://localhost:3000`

## Architecture

### Backend (`/backend`)

- **app.py** - Main FastAPI application with endpoints
- **database.py** - SQLAlchemy models and database setup
- **schemas.py** - Pydantic request/response models

**API Endpoints:**
- `POST /benchmark/run` - Start a new benchmark
- `GET /benchmark/{run_id}` - Get results for a specific run
- `GET /benchmarks` - List all benchmarks
- `GET /benchmarks/compare` - Compare multiple runs
- `GET /models` - Get available models

### Frontend (`/frontend`)

- **src/pages/** - Main pages (Dashboard, BenchmarkDetail, Compare)
- **src/components/** - Reusable components
- **src/api/** - API client for backend communication
- **src/styles/** - CSS stylesheets

## Supported Models

Currently supports:
- **Groq**: `llama-3.1-70b-versatile`, `llama-3.1-8b-instant`
- **GitHub Models**: `gpt-4o-mini`
- **Google Gemini**: `gemini-2.0-flash`
- **Ollama**: `llama3.1:8b` (local)

## Configuration

Create a `.env` file (copy from `.env.example`):

```bash
GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=your_github_token
GOOGLE_API_KEY=your_google_api_key
DATASET_PATH=data/dataset.jsonl
```

## Database

Results are stored in SQLite (`benchmarks.db`). Each benchmark run includes:
- Run ID and timestamp
- Dataset path
- Complete results for each test
- Summary statistics by model

To view the database:
```bash
sqlite3 benchmarks.db "SELECT * FROM benchmark_runs;"
```

## File Structure

```
.
├── backend/
│   ├── app.py              # FastAPI application
│   ├── database.py         # Database models
│   ├── schemas.py          # Pydantic schemas
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   ├── api/            # API client
│   │   └── styles/         # CSS files
│   ├── public/
│   └── package.json        # Node dependencies
├── eval/                   # Benchmark evaluation modules
├── providers/              # LLM provider implementations
├── data/                   # Datasets and results
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-container setup
└── README.md              # This file
```

## Running Benchmarks

### Via Web UI

1. Open `http://localhost:3000`
2. Select models to benchmark
3. Click "Start Benchmark"
4. Monitor progress in the UI
5. View results and charts once complete

### Via API

```bash
# Start a benchmark
curl -X POST http://localhost:8000/benchmark/run \
  -H "Content-Type: application/json" \
  -d '{"dataset_path": "data/dataset.jsonl"}'

# Expected response:
# {"run_id": "a1b2c3d4", "status": "started", ...}

# Get results
curl http://localhost:8000/benchmark/a1b2c3d4
```

## Performance & Results

Results include:
- **Accuracy**: Exact match percentage
- **Grounded**: Non-hallucination score
- **Token Usage**: Input and output token counts
- **Latency**: Response time metrics (if logged)

Results are persisted to database and can be:
- Viewed in the dashboard
- Exported as JSON
- Compared across multiple runs

## Deployment

### AWS EC2

```bash
git clone https://github.com/yourusername/llm-eval-framework.git
cd llm-eval-framework
docker-compose up -d
```

### Google Cloud Run

```bash
gcloud run deploy llm-eval-backend \
  --source . \
  --platform managed \
  --region us-central1
```

### Heroku

```bash
heroku create llm-eval
git push heroku main
```

## Development

### Adding a New LLM Provider

1. Create a new provider in `providers/`:

```python
from providers.base import BaseProvider, LLMResponse

class MyProvider(BaseProvider):
    def __init__(self):
        pass
    
    def complete(self, question: str) -> LLMResponse:
        # Implement API call
        return LLMResponse(
            text=response_text,
            input_tokens=input_count,
            output_tokens=output_count
        )
```

2. Register in `backend/app.py`:

```python
PROVIDERS = {
    "my-model": lambda: MyProvider(),
    ...
}
```

### Adding a New Dashboard Component

1. Create component in `frontend/src/components/`
2. Import and use in pages
3. Add styling to `frontend/src/styles/`

## Troubleshooting

### API Connection Failed
- Ensure backend is running on `http://localhost:8000`
- Check firewall/port settings
- Verify environment variables are set

### Benchmark Hangs
- Check API key validity
- Verify dataset path is correct
- Check backend logs for errors

### Results Not Saving
- Ensure `benchmarks.db` is writable
- Check disk space
- Verify SQLite is installed

## Contributing

Contributions welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review example results in `/data/results/`

## Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Export to CSV/PDF
- [ ] Model fine-tuning integration
- [ ] A/B testing framework
- [ ] Cost analytics dashboard
- [ ] Multi-user support with authentication
- [ ] Webhook notifications
- [ ] Model registry with versioning

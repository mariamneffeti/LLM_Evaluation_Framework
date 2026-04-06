from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.benchmark import run_benchmark
from eval.reporter import report_results
from providers.groq_provider import GroqProvider
from providers.github_provider import GithubModelsProvider
from providers.ollama_provider import OllamaProvider
from providers.gemini_provider import GeminiProvider

from database import SessionLocal, engine, Base, get_db, BenchmarkRun
from schemas import BenchmarkRequest, BenchmarkRunResponse, BenchmarkSummary

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LLM Evaluation Framework API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model providers
PROVIDERS = {
    "llama-3.1-70b-versatile": lambda: GroqProvider(api_key=os.getenv("GROQ_API_KEY")),
    "gpt-4o-mini": lambda: GithubModelsProvider(),
    "gemini-2.0-flash": lambda: GeminiProvider(),
    "llama3.1:8b": lambda: OllamaProvider(),
}


def calculate_summary(results: list) -> dict:
    """Calculate summary statistics from benchmark results."""
    if not results:
        return {}
    
    grouped = {}
    for result in results:
        model = result['model']
        if model not in grouped:
            grouped[model] = []
        grouped[model].append(result)
    
    summary = {}
    for model, runs in grouped.items():
        summary[model] = {
            "accuracy": sum(r.get('accuracy', 0) for r in runs) / len(runs) if runs else 0,
            "grounded": sum(r.get('hallucination', 0) for r in runs) / len(runs) if runs else 0,
            "avg_input_tokens": sum(r.get('input_tokens', 0) for r in runs) / len(runs) if runs else 0,
            "avg_output_tokens": sum(r.get('output_tokens', 0) for r in runs) / len(runs) if runs else 0,
            "total_results": len(runs)
        }
    
    return summary


def run_benchmark_task(run_id: str, dataset_path: str, model_names: list, db: Session):
    """Background task to run benchmark."""
    try:
        candidates = []
        for model_name in model_names:
            if model_name in PROVIDERS:
                candidates.append((model_name, PROVIDERS[model_name]()))
        
        if not candidates:
            print(f"[{run_id}] No valid models specified")
            return
        
        print(f"[{run_id}] Starting benchmark with {len(candidates)} models")
        results = run_benchmark(dataset_path, candidates)
        summary = calculate_summary(results)
        
        # Save to database
        run = BenchmarkRun(
            run_id=run_id,
            dataset_path=dataset_path,
            results=results,
            summary=summary
        )
        db.add(run)
        db.commit()
        print(f"[{run_id}] Benchmark completed and saved")
    except Exception as e:
        print(f"[{run_id}] Error: {str(e)}")


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "LLM Evaluation Framework API", "version": "1.0.0"}


@app.get("/models")
def get_available_models():
    """Get list of available models."""
    return {
        "models": list(PROVIDERS.keys()),
        "count": len(PROVIDERS)
    }


@app.post("/benchmark/run")
def run_benchmark_endpoint(request: BenchmarkRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Start a new benchmark run."""
    run_id = str(uuid.uuid4())[:8]
    
    # Use all models if not specified
    model_names = request.models or list(PROVIDERS.keys())
    
    # Validate models
    invalid_models = [m for m in model_names if m not in PROVIDERS]
    if invalid_models:
        raise HTTPException(status_code=400, detail=f"Invalid models: {invalid_models}")
    
    # Add background task
    background_tasks.add_task(run_benchmark_task, run_id, request.dataset_path, model_names, db)
    
    return {
        "run_id": run_id,
        "status": "started",
        "models": model_names,
        "message": "Benchmark started in background. Check status endpoint for progress."
    }


@app.get("/benchmark/{run_id}")
def get_benchmark_result(run_id: str, db: Session = Depends(get_db)):
    """Get benchmark results by run_id."""
    run = db.query(BenchmarkRun).filter(BenchmarkRun.run_id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail=f"Benchmark run '{run_id}' not found")
    
    # Return plain dict instead of validated schema to avoid type errors
    return {
        "run_id": run.run_id,
        "timestamp": run.timestamp.isoformat() if run.timestamp else None,
        "dataset_path": run.dataset_path,
        "results": run.results,  # Already a list of dicts from JSON
        "summary": run.summary
    }


@app.get("/benchmarks")
def list_benchmarks(limit: int = 20, db: Session = Depends(get_db)):
    """List all benchmark runs."""
    runs = db.query(BenchmarkRun).order_by(BenchmarkRun.timestamp.desc()).limit(limit).all()
    
    summaries = []
    for run in runs:
        summaries.append({
            "run_id": run.run_id,
            "timestamp": run.timestamp,
            "dataset_path": run.dataset_path,
            "models": list(run.summary.keys()) if run.summary else [],
            "summary": run.summary
        })
    
    return {"runs": summaries, "total": len(summaries)}


@app.get("/benchmarks/compare")
def compare_benchmarks(run_ids: str, db: Session = Depends(get_db)):
    """Compare multiple benchmark runs."""
    run_id_list = run_ids.split(",")
    
    runs = []
    for run_id in run_id_list:
        run = db.query(BenchmarkRun).filter(BenchmarkRun.run_id == run_id.strip()).first()
        if run:
            runs.append({
                "run_id": run.run_id,
                "timestamp": run.timestamp,
                "summary": run.summary
            })
    
    if not runs:
        raise HTTPException(status_code=404, detail="No benchmark runs found")
    
    return {"runs": runs}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

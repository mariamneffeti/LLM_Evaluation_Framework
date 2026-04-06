from providers.groq_provider import GroqProvider
from providers.github_provider import GithubModelsProvider
from providers.ollama_provider import OllamaProvider
from eval.benchmark import run_benchmark
from eval.reporter import report_results
import os
CANDIDATES = [
    ("llama-3.1-70b-versatile", GroqProvider(api_key=os.getenv("GROQ_API_KEY"))),
    ("gpt-4o-mini",             GithubModelsProvider()),
    ("llama3.1:8b",             OllamaProvider()),
]

if __name__ == "__main__":
    results = run_benchmark("data/dataset.jsonl", CANDIDATES)
    report_results(results)
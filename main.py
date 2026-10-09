from providers.groq_provider import GroqProvider
from providers.ollama_provider import OllamaProvider
from eval.benchmark import run_benchmark
from eval.reporter import report_results
import os
CANDIDATES = [
    ("openai/gpt-oss-20b", GroqProvider(api_key=os.getenv("GROQ_API_KEY"))),
    ("llama3.1:8b",             OllamaProvider()),
]

if __name__ == "__main__":
    results = run_benchmark("data/dataset.jsonl", CANDIDATES)
    report_results(results)

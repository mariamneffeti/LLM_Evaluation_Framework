import re
import json
from pathlib import Path
from datetime import datetime
from .scorer import score_accuracy, score_hallucination, score_tokens


def load_dataset(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]

def run_benchmark(dataset_path : str, candidates: list[tuple]) -> list[dict]:
    dataset = load_dataset(dataset_path)
    all_results = []
    for model_name, provider in candidates:
        print(f"Running benchmark for {model_name}...")
        for item in dataset:
            try:
                response = provider.complete(item['question'])
                result = {
                    'model': model_name,
                    'question_id': item['id'],
                    'question': item['question'],
                    'expected': item.get('expected', ''),
                    'response': response.text,
                    'input_tokens': response.input_tokens,
                    'output_tokens': response.output_tokens
                }
                result['accuracy'] = score_accuracy(result)
                result['hallucination'] = score_hallucination(result)
                result['tokens'] = score_tokens(result)
                print(
                    f"  [{item['id']}] "
                    f"input_tokens={response.input_tokens} "
                    f"output_tokens={response.output_tokens}"
                )
                all_results.append(result)
            except Exception as e:
                print(f"Error processing item {item['id']} with model {model_name}: {e}")
    if all_results:
        _save_results(all_results, dataset_path)
    return all_results
def _save_results(results : list, dataset_path):
    output_dir = Path(dataset_path).parent / "results"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"run_{timestamp}.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_path}")

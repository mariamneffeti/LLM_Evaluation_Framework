from collections import defaultdict

def report_results(results : list):
    grouped = defaultdict(list)
    for result in results:
        grouped[result['model']].append(result)
    print(f"\n{'Model':<25} {'Accuracy':>10} {'Grounded':>10} {'Avg Tokens':>14}")
    print("-" * 70)
    for model, runs in grouped.items():
        avg_accuracy = sum(r.get('accuracy', 0) for r in runs) / len(runs) if runs else 0
        avg_hallucination = sum(r.get('hallucination', 0) for r in runs) / len(runs) if runs else 0
        avg_tokens = sum(r.get('input_tokens', 0) + r.get('output_tokens', 0) for r in runs) / len(runs) if runs else 0
        print(f"{model:<25} {avg_accuracy:>10.2%} {avg_hallucination:>10.2%} {avg_tokens:>14.0f}")

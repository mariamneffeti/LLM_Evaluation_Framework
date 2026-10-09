from eval.benchmark import run_benchmark
from providers.base import LLMResponse


class FakeProvider:
    def complete(self, question):
        assert question == "What is 2 + 2?"
        return LLMResponse(text="4", input_tokens=5, output_tokens=1)


def test_benchmark_scores_mocked_provider_without_api_calls(tmp_path):
    dataset = tmp_path / "dataset.jsonl"
    dataset.write_text(
        '{"id":"q1","question":"What is 2 + 2?","expected":"4"}\n',
        encoding="utf-8",
    )

    results = run_benchmark(str(dataset), [("fake-model", FakeProvider())])

    assert len(results) == 1
    result = results[0]
    assert result["model"] == "fake-model"
    assert result["response"] == "4"
    assert result["accuracy"] == 1.0
    assert result["hallucination"] == 1.0
    assert result["tokens"] == {
        "input_tokens": 5,
        "output_tokens": 1,
        "total_tokens": 6,
    }

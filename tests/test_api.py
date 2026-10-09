from fastapi.testclient import TestClient

import app as api


client = TestClient(api.app)


def test_root_and_health_endpoints():
    assert client.get("/").json() == {
        "message": "LLM Evaluation Framework API",
        "version": "1.0.0",
    }
    assert client.get("/health").json() == {"status": "healthy"}


def test_models_endpoint_lists_configured_providers(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-groq-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key")
    response = client.get("/models")

    assert response.status_code == 200
    assert response.json() == {
        "models": [
            "openai/gpt-oss-20b",
            "gpt-4o-mini",
            "gemini-3.8-flash",
            "llama3.1:8b",
        ],
        "count": 4,
    }


def test_benchmark_run_accepts_payload_without_running_provider(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-groq-key")
    monkeypatch.setattr(api, "run_benchmark_task", lambda *args: None)

    response = client.post(
        "/benchmark/run",
        json={"dataset_path": "data/dataset.jsonl", "models": ["openai/gpt-oss-20b"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["run_id"]
    assert body["status"] == "started"
    assert body["models"] == ["openai/gpt-oss-20b"]


def test_benchmark_endpoint_returns_result_structure(monkeypatch):
    class FakeQuery:
        def filter(self, *_args):
            return self

        def first(self):
            return type(
                "Run",
                (),
                {
                    "run_id": "test1234",
                    "timestamp": None,
                    "dataset_path": "data/dataset.jsonl",
                    "results": [{"model": "gpt-4o-mini", "accuracy": 1.0, "response": "ok"}],
                    "summary": {"gpt-4o-mini": {"accuracy": 1.0}},
                },
            )()

    class FakeDB:
        def query(self, _model):
            return FakeQuery()

    api.app.dependency_overrides[api.get_db] = lambda: FakeDB()
    try:
        response = client.get("/benchmark/test1234")
    finally:
        api.app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "run_id": "test1234",
        "timestamp": None,
        "dataset_path": "data/dataset.jsonl",
        "results": [{"model": "gpt-4o-mini", "accuracy": 1.0, "response": "ok"}],
        "summary": {
            "gpt-4o-mini": {
                "accuracy": 1.0,
                "grounded": 0.0,
                "avg_input_tokens": 0.0,
                "avg_output_tokens": 0.0,
                "total_results": 1,
            }
        },
        "error": None,
    }

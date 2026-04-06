from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class ResultItem(BaseModel):
    model: str
    question_id: str
    question: str
    expected: str
    response: str
    input_tokens: int
    output_tokens: int
    accuracy: float
    hallucination: float
    tokens: Dict[str, int]


class BenchmarkRunResponse(BaseModel):
    id: int
    run_id: str
    timestamp: datetime
    dataset_path: str
    results: List[ResultItem]
    summary: Dict[str, Dict[str, float]]

    class Config:
        from_attributes = True


class BenchmarkSummary(BaseModel):
    run_id: str
    timestamp: datetime
    models: List[str]
    summary: Dict[str, Dict[str, float]]


class BenchmarkRequest(BaseModel):
    dataset_path: str = "data/dataset.jsonl"
    models: Optional[List[str]] = None

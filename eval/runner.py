import time
import anthropic
import openai
from dataclasses import dataclass



@dataclass
class RunResult:
    model : str
    question_id : str
    question : str
    expected : str
    response : str
    latency_ms : float
    input_tokens : int
    output_tokens : int

def run_anthropic(client, model, item):
    start_time = time.perf_counter()
    response = client.messages.create(
        model=model,
        max_tokens=512,
        msg=[
            {"role": "user", "content": item["question"]}
        ])
    latency_ms = (time.perf_counter() - start_time) * 1000
    return RunResult(
        model=model,
        question_id=item["question_id"],
        question=item["question"],
        expected=item["expected"],
        response=msg.content[0].text,
        latency_ms=round(latency_ms, 2),
        input_tokens=msg.usage.input_tokens,
        output_tokens=msg.usage.output_tokens
    )
def run_openai(client, model, item):
    start_time = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        max_tokens=512,
        messages=[
            {"role": "user", "content": item["question"]}
        ]
    )
    latency_ms = (time.perf_counter() - start_time) * 1000
    return RunResult(
        model=model,
        question_id=item["question_id"],
        question=item["question"],
        expected=item["expected"],
        response=response.choices[0].message.content,
        latency_ms=round(latency_ms, 2),
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens
    )

import ollama
import json
import time
import tiktoken
from pathlib import Path

enc = tiktoken.get_encoding("cl100k_base")

# clear results file
Path("results").mkdir(exist_ok=True)
with open("results/results.json", "w") as f:
    json.dump([], f)

with open("prompts/prompt.json","r") as f:
    prompt_data=json.load(f)

results = []

for test in prompt_data["tests"]:

    prompt_type = test["type"]
    prompt = test["prompt"]
    expected = test.get("expected_answer","")

    prompt_tokens = len(enc.encode(prompt))

    start = time.time()

    response = ollama.chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}]
    )

    end = time.time()

    answer = response["message"]["content"]

    response_tokens = len(enc.encode(answer))

    # evaluation
    is_correct = expected.lower() in answer.lower()

    result = {
        "test_type": prompt_type,
        "prompt": prompt,
        "response": answer,
        "expected_answer": expected,
        "correct": is_correct,
        "prompt_tokens": prompt_tokens,
        "response_tokens": response_tokens,
        "latency": round(end - start, 2)
    }

    results.append(result)

with open("results/results.json", "w") as f:
    json.dump(results, f, indent=4)

print("✅ Tests completed. Results saved in results/results.json")
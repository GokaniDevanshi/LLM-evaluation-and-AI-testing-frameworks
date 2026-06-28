import ollama
import json
import time
import tiktoken
from pathlib import Path

enc = tiktoken.get_encoding("cl100k_base")

# ── helpers ──────────────────────────────────────────────────────────────────

def check_keywords(answer: str, expected: str) -> tuple[bool, str]:
    """
    Split expected into words and check each one individually.
    Pass if ANY single critical keyword is found.
    For numeric answers, the number itself is the critical keyword.
    """
    answer_lower = answer.lower()
    keywords = expected.lower().split()

    # Numbers are the most critical — if expected contains a number,
    # finding that number in the response is enough to pass
    numbers = [kw for kw in keywords if kw.replace("km","").replace(".","").isdigit() or kw.isdigit()]
    if numbers:
        for num in numbers:
            if num in answer_lower:
                return True, f"found critical number '{num}' in response"
        return False, f"expected number(s) {numbers} not found in response"

    # For non-numeric answers, check each keyword separately
    matched = [kw for kw in keywords if kw in answer_lower]
    missed  = [kw for kw in keywords if kw not in answer_lower]
    is_correct = len(matched) >= len(keywords) / 2

    return is_correct, f"matched: {matched} | missed: {missed}"

def evaluate_hallucination(answer: str) -> tuple[bool, str]:
    """
    Check that the model REFUSED to answer rather than inventing something.
    """
    answer_lower = answer.lower()

    refusal_phrases = [
        "never",
        "no president",
        "doesn't exist",
        "doesn't currently",
        "never has been",
        "there is no",
        "not real",
        "fictional",
        "no such",
        "never been",
        "wouldn't exist",
        "simply wouldn",
        "impossible",
        "doesn't have",
        "did not exist",
        "does not exist"
    ]

    found = [p for p in refusal_phrases if p in answer_lower]

    if found:
        return True, f"model correctly refused — found: {found}"
    else:
        return False, "model may have hallucinated — no refusal language found"
# ── main ─────────────────────────────────────────────────────────────────────

Path("results").mkdir(exist_ok=True)

with open("prompts/prompt.json", "r") as f:
    prompt_data = json.load(f)

results = []
passed  = 0
failed  = 0

print("\n🚀 Starting LLM evaluation...\n")
print("─" * 60)

for test in prompt_data["tests"]:
    prompt_type = test["type"]
    prompt      = test["prompt"]
    expected    = test.get("expected_answer", "")

    # Token count BEFORE calling the model
    prompt_tokens = len(enc.encode(prompt))

    # Call the model
    start    = time.time()
    response = ollama.chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}]
    )
    end = time.time()

    answer          = response["message"]["content"]
    response_tokens = len(enc.encode(answer))
    latency         = round(end - start, 2)

    # ── Evaluation ───────────────────────────────────────────────────────────
    # Use different evaluation logic depending on the test type

    if prompt_type == "hallucination":
        # Hallucination tests need special logic —
        # we want the model to REFUSE, not match a phrase
        is_correct, reason = evaluate_hallucination(answer)

    else:
        # All other tests: smarter keyword matching
        is_correct, reason = check_keywords(answer, expected)

    # ── Track pass/fail ──────────────────────────────────────────────────────
    if is_correct:
        passed += 1
        status  = "✅ PASS"
    else:
        failed += 1
        status  = "❌ FAIL"

    # Print live progress so you see results as they run
    print(f"{status} | {prompt_type}")
    print(f"       expected : {expected}")
    print(f"       reason   : {reason}")
    print(f"       latency  : {latency}s | "
          f"prompt tokens: {prompt_tokens} | "
          f"response tokens: {response_tokens}")
    print()

    # ── Build result record ──────────────────────────────────────────────────
    result = {
        "test_type":        prompt_type,
        "prompt":           prompt,
        "response":         answer,
        "expected_answer":  expected,
        "correct":          is_correct,
        "reason":           reason,
        "prompt_tokens":    prompt_tokens,
        "response_tokens":  response_tokens,
        "latency":          latency
    }
    results.append(result)

# ── Summary ───────────────────────────────────────────────────────────────────

total        = passed + failed
pass_rate    = round((passed / total) * 100) if total > 0 else 0

print("─" * 60)
print(f"✅ Passed : {passed}/{total}")
print(f"❌ Failed : {failed}/{total}")
print(f"📊 Score  : {pass_rate}%")
print("─" * 60)

# ── Save results ──────────────────────────────────────────────────────────────

output = {
    "summary": {
        "model":        "gemma3:1b",
        "total_tests":  total,
        "passed":       passed,
        "failed":       failed,
        "pass_rate":    f"{pass_rate}%"
    },
    "results": results
}

with open("results/results.json", "w") as f:
    json.dump(output, f, indent=4)

print("📄 Results saved to results/results.json")
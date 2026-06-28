# LLM Prompt Testing Framework

A lightweight Python framework for evaluating Large Language Model responses
across different prompt types — with automated correctness checks, token
counting, latency measurement, and structured JSON reporting.

Built as a foundation for CI-native LLM quality testing.

---

## What It Does

Runs a suite of prompt tests against a local LLM (via Ollama) and evaluates
each response against expected outcomes. Results are saved as structured JSON
with a pass/fail summary.

---

## Test Types Supported

| Type | What It Tests |
|---|---|
| `zero_shot` | Direct factual questions with no examples |
| `few_shot` | Pattern recognition from in-context examples |
| `chain_of_thought` | Step-by-step reasoning and math |
| `hallucination` | Whether the model refuses impossible questions |
| `tokenization` | Word and token counting accuracy |
| `context_window` | Summarization of provided text |

---

---

## Setup

**1. Install Ollama**

Download from https://ollama.com and install for your OS.

**2. Pull a model**

```bash
ollama pull gemma3:1b
```

**3. Install Python dependencies**

```bash
pip install ollama tiktoken
```

**4. Run the evaluation**

```bash
python llm_test.py
```

---

## Output

Terminal output shows live results as each test runs:

## Changing the Model

To test a different Ollama model, change line in `llm_test.py`:

```python
# Change this
model="gemma3:1b"

# To any model you have pulled locally
model="llama3.2:3b"
model="mistral:7b"
model="phi3:mini"
```

## Roadmap

- [ ] LLM-as-Judge scoring for semantic quality evaluation
- [ ] HTML report generation
- [ ] Baseline snapshot and regression detection
- [ ] GitHub Actions CI integration
- [ ] Multi-model comparison mode
- [ ] Support for Claude and GPT via API

---

## Tech Stack

- Python 3.10+
- [Ollama](https://ollama.com) — local LLM inference
- [tiktoken](https://github.com/openai/tiktoken) — token counting
- gemma3:1b — default evaluation model
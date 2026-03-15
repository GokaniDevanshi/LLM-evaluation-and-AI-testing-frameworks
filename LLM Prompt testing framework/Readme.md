# LLM Prompt Testing Framework

## Overview

This project is a **Python-based LLM evaluation framework** designed to test and evaluate prompt responses from local Large Language Models (LLMs).

The framework dynamically loads prompts from JSON files, sends them to a locally running LLM using **Ollama**, captures the responses, and evaluates them against expected answers. It also records important evaluation metrics such as **accuracy, latency, and token usage**.

This project demonstrates basic concepts used in **LLM testing, prompt evaluation, and AI quality assurance**.

---

## Features

* Prompt-based evaluation using JSON test cases
* Automated execution of prompts against a local LLM
* Evaluation of responses against expected answers
* Latency measurement for each prompt
* Token counting for prompts and responses
* Result logging in structured JSON format
* Modular and easily extendable design

---

## Technologies Used

* Python
* Ollama (for running local LLMs)
* tiktoken (for tokenization)
* JSON for prompt storage and result logging
* pathlib for file handling

---

## Project Structure

```
LLM-Prompt-Testing-Framework
│
├── prompts
│   └── prompt.json          # Contains prompt test cases
│
├── results
│   └── results.json         # Stores evaluation results
│
├── llm_test.py              # Main evaluation script
│
└── README.md
```

---

## Example Prompt Test File

`prompts/prompt.json`

```json
{
  "tests": [
    {
      "type": "zero_shot",
      "prompt": "What is the capital of Germany?",
      "expected_answer": "Berlin"
    },
    {
      "type": "hallucination",
      "prompt": "Who was the president of Mars in 1995?",
      "expected_answer": "There was no president of Mars"
    }
  ]
}
```

---

## How It Works

1. Prompts are stored in a JSON file.
2. The script loads the prompts dynamically.
3. Each prompt is sent to the LLM through Ollama.
4. The response is captured and compared with the expected answer.
5. Evaluation metrics are computed.
6. Results are saved to `results/results.json`.

---

## Metrics Captured

| Metric          | Description                                         |
| --------------- | --------------------------------------------------- |
| Accuracy        | Whether the expected answer appears in the response |
| Latency         | Time taken for the model to generate a response     |
| Prompt Tokens   | Number of tokens in the input prompt                |
| Response Tokens | Number of tokens in the generated response          |

---

## Example Output

```json
{
  "test_type": "zero_shot",
  "prompt": "What is the capital of Germany?",
  "response": "The capital of Germany is Berlin.",
  "expected_answer": "Berlin",
  "correct": true,
  "prompt_tokens": 7,
  "response_tokens": 12,
  "latency": 1.42
}
```

---

## Setup Instructions

### 1 Install Dependencies

```bash
pip install ollama tiktoken
```

Install and run Ollama from:

https://ollama.com

### 2 Pull a Model

```bash
ollama pull gemma3:1b
```

### 3 Run the Evaluation Script

```bash
python llm_test.py
```

Results will be generated in:

```
results/results.json
```

---

## Example Prompt Types Tested

* Zero-shot prompts
* Few-shot prompts
* Chain-of-thought reasoning
* Hallucination checks
* Tokenization understanding
* Context summarization

---

## Future Improvements / Next Steps

Planned enhancements for this framework include:

### Multi-Model Evaluation

Extend the framework to compare responses across multiple LLMs such as:

* Gemma
* Llama
* Mistral

This will allow benchmarking models on:

* Accuracy
* Latency
* Token usage
* Hallucination rate

Example comparison output:

| Model   | Accuracy | Avg Latency |
| ------- | -------- | ----------- |
| gemma   | 66%      | 2.1s        |
| llama   | 83%      | 3.4s        |
| mistral | 79%      | 2.8s        |

### Additional Improvements

* Automated hallucination detection
* Response quality scoring
* Prompt dataset expansion
* Visualization dashboards for evaluation results
* Integration with CI/CD pipelines for automated LLM testing

---

## Learning Outcomes

This project helped explore:

* Prompt engineering concepts
* LLM evaluation techniques
* Tokenization and token counting
* Latency measurement
* AI testing workflows

---

## Author

Developed as a learning project to explore **LLM evaluation and AI testing frameworks**.

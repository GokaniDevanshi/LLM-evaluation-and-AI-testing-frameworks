# LLM Evaluation – Learning Notes

This weekend, I started learning about **LLM evaluation** to build a deeper understanding of how language models are assessed and what makes an evaluation reliable.

## What is LLM Evaluation?

LLM evaluation is the **systematic process of assessing a model's performance**.

It measures how well a model performs specific tasks using metrics such as:

* Accuracy
* Reliability
* Cost
* Scalability
* Latency

## Why Do We Evaluate?

We evaluate models to:

* Track improvements over time (Is the model getting better?)
* Measure trustworthiness and reliability
* Compare different models or prompting methods
* Determine whether a model is suitable for production
* Ensure the model meets predefined quality standards

## What Are We Evaluating?

### 1. Generative Tasks

Tasks where the model creates new content, such as:

* Answering open-ended questions
* Summarizing documents
* Writing emails or articles
* Generating code

### 2. Understanding Tasks

Tasks where the model interprets or classifies information, such as:

* Text classification
* Information retrieval
* Sentiment analysis
* Named Entity Recognition (NER)

## How Do We Evaluate?

### 1. Reference-Based (Ground Truth)

Compare the model's output against a known correct answer.

### 2. Rule-Based / Rubric Evaluation

Use predefined criteria (rubrics) to evaluate qualities such as:

* Correctness
* Relevance
* Completeness
* Clarity
* Safety

This approach is especially useful for evaluating free-text responses.

### 3. Threshold-Based Evaluation

Define acceptable performance thresholds before deployment.

Example:

* Accuracy ≥ 95%
* Response latency < 2 seconds

If the model meets the threshold, it is considered acceptable for the intended use case.

## Common Evaluation Metrics

### Accuracy

Measures the percentage of correct predictions.

**Example:**
If an AI recommends products and 90 out of 100 recommendations are correct, the accuracy is **90%**.

Best suited for:

* Classification tasks

---

### Precision

Measures how many predicted positive results are actually positive.

**Focus:** Minimize **false positives**.

**Example:**
In spam detection, high precision ensures important emails are not incorrectly marked as spam.

---

### Recall

Measures how many actual positive cases the model successfully identifies.

**Focus:** Minimize **false negatives**.

**Example:**
In medical diagnosis, high recall is essential because missing a disease can have serious consequences.

---

### F1 Score

The harmonic mean of **Precision** and **Recall**.

Useful when both false positives and false negatives are important.

**Example:**
Fraud detection systems, where both catching fraud and avoiding false alarms matter.

---

### BLEU Score

Compares generated text with one or more reference responses.

Commonly used for:

* Machine translation
* Text generation

**Limitation:** It compares exact word overlap and may not fully capture semantic meaning.

---

### Human Evaluation

Humans assess outputs based on factors such as:

* Coherence
* Relevance
* Helpfulness
* Fluency
* Safety

This is especially valuable for open-ended generative tasks.

---

### Semantic Similarity

Evaluates whether two responses have the same meaning, even if different words are used.

Unlike BLEU, it focuses on **meaning rather than exact wording**.

---

### Latency

Measures **how quickly** the model generates a response.

Lower latency generally provides a better user experience.

---

### Throughput

Measures **how many requests or predictions** a model can process within a given time.

Important for applications serving many users simultaneously.

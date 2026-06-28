# Day 01 — LLM Prompt Testing Basics

**Date:** 27 June 2026  
**Project:** LLM Prompt Testing Framework  
**Commit:** day 1: working LLM evaluation framework with 6 prompt types
---

My Earlier build had an issues- **Evaluation Logic Was Too Strict**
- Smarter keyword matching — check for key words separately, not as one phrase
- Add a summary at the end — pass/fail count printed to terminal
- Better results.json — add a summary section so it's readable

## What I Built Today

A Python script that runs 6 prompt types against a local LLM (gemma3:1b via 
Ollama) and evaluates each response automatically.

Prompt types tested:
- zero_shot — direct factual question, no examples
- few_shot — pattern learned from in-context examples
- chain_of_thought — step by step reasoning
- hallucination — model should refuse impossible questions
- tokenization — word counting accuracy
- context_window — summarization

---

## What I Learned Today

### 1. LLM outputs are non-deterministic
Traditional testing uses exact match: `assert response == "Berlin"`.
This breaks with LLMs because the same prompt gives different responses
every run. The model might say "The capital is Berlin" or "Berlin is the
capital" — both correct, neither matches exactly.

**Solution I built:** Split expected answer into keywords and check each
one separately instead of matching the whole phrase.

### 2. Different test types need different evaluation logic
You cannot use one evaluation strategy for everything.

| Test type | Why it needs different logic |
|---|---|
| Factual (zero_shot) | Check if key answer word appears |
| Numeric (chain_of_thought) | Check if the number appears anywhere |
| Hallucination | Check model REFUSED, not what it said |
| Summarization | Check if key concepts are present |

### 3. Small models have measurable, real limitations
gemma3:1b results:

| Test | Pass? | Why |
|---|---|---|
| zero_shot | ✅ | Simple recall, model handles well |
| few_shot | ✅ | Pattern following from examples |
| chain_of_thought | ✅ | Got 180km correct |
| hallucination | ✅ | Correctly refused to answer |
| tokenization | ❌ | Said 9 words, correct answer is 5 |
| context_window | ❌ | Asked for text that was already there |

A 1 billion parameter model is genuinely too small for precise counting
and context tasks. This framework makes that measurable instead of just
a feeling.

### 4. What tiktoken actually does
tiktoken counts how many tokens a string uses. Tokens are not words —
they are chunks the model sees internally.

Example:
- "Berlin" = 1 token
- "Artificial" = 2 tokens (Artif + icial)
- "transforming" = 2 tokens

I used tiktoken to measure prompt size and response size. This matters
for cost estimation when using paid APIs — you pay per token, not per word.

### 5. Latency varies a lot by response length
Observed today:
- Short responses (1-2 sentences): 0.9s — 2.7s
- Long responses (with step by step reasoning): 4.2s — 22s

The model generates one token at a time. More tokens = more time.
This is called autoregressive generation.

---

## Concepts I Still Don't Fully Understand

- [ ] How exactly does Ollama serve the model locally?
- [ ] What is the difference between temperature 0 and temperature 1?
- [ ] How does few-shot prompting actually change what the model does internally?
- [ ] What makes a good rubric for LLM-as-Judge evaluation?

---

## What I Want To Build Next

- [ ] LLM-as-Judge: use a second LLM to score response quality 0-10
- [ ] HTML report so results are readable without opening JSON
- [ ] Baseline snapshots: save today's scores, compare tomorrow's run
- [ ] GitHub Actions: run this automatically on every commit
- [ ] Try the same prompts on a bigger model (llama3.2:3b) and compare

---

## Resources I Used Today

- Ollama docs: https://ollama.com
- tiktoken: https://github.com/openai/tiktoken
- gemma3 model: https://ollama.com/library/gemma3

---

## One Thing I Would Tell Myself This Morning

> "The model getting the right answer in the wrong format is YOUR
> evaluation problem, not the model's problem. Test what you actually
> care about, not the exact words."
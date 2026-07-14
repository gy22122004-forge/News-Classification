---
title: News Classifier — Transformer Demo
emoji: 📰
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
tags:
  - nlp
  - text-classification
  - transformers
  - zero-shot-classification
  - fastapi
  - bart
pinned: false
license: mit
---

# 📰 News Classifier — Transformer Model Demo

A working demo of **zero-shot news classification** using `facebook/bart-large-mnli` — a Transformer model (BART-large) fine-tuned on Multi-Genre NLI (MNLI).

**Demo by Gaurav Yadav** · AI Demo Programmer · Business Optima Assignment

---

## What It Does

Classifies any news article into **8 categories** with no labelled training data required:

`Politics` · `Sports` · `Business` · `Technology` · `Health` · `Entertainment` · `Science` · `World News`

---

## How It Works

1. **Input**: Paste any news article text
2. **Model**: `facebook/bart-large-mnli` (406M parameters, BART-large fine-tuned on MNLI)
3. **Zero-shot NLI**: For each category label, the model scores: *"This text is about {label}"*
4. **Output**: Confidence scores for all 8 categories, ranked by probability

---

## Architecture

Based on **"Attention Is All You Need"** (Vaswani et al., 2017):

```
Input Text → BPE Tokenizer → Embedding + Positional Encoding
    → 12× [Multi-Head Self-Attention → Add&Norm → FFN → Add&Norm]
    → NLI Head → Entailment Scores → Top Category
```

Core formula: `Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V`

---

## API

- `GET /health` — Health check
- `POST /classify` — Classify news text

```bash
curl -X POST https://Gaurav2212-news-classifier.hf.space/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple unveiled its new M4 chip with built-in AI neural engine."}'
```

---

## Stack

| Layer | Technology |
|---|---|
| ML Model | `facebook/bart-large-mnli` (Hugging Face Transformers) |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML · CSS · JavaScript |
| Deployment | Hugging Face Spaces (Docker) |

---

## References

- Vaswani et al. (2017) — [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Lewis et al. (2019) — [BART: Denoising Seq-to-Seq Pre-training](https://arxiv.org/abs/1910.13461)
- [facebook/bart-large-mnli on Hugging Face](https://huggingface.co/facebook/bart-large-mnli)

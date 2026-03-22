# Information Retrieval System

## Overview

This project implements an **Information Retrieval system** using:

* Boolean Model
* Vector Space Model (TF-IDF + Cosine Similarity)
* Chatbot with LLM (LLaMA via Ollama)

It retrieves and ranks documents from a collection and compares the performance of different retrieval approaches.

---

## Features

* Boolean queries (`AND`, `OR`, `NOT`)
* Ranked retrieval with VSM
* Evaluation (precision, recall, time)
* Chatbot based on retrieved documents

---

## Structure

```
preprocess.py   # Build indexes
boolean.py      # Boolean model
vsm.py          # VSM model
metrics.py      # Evaluation
chatbot.py      # LLM chatbot
```

---

## Usage

```bash
python preprocess.py
python boolean.py
python vsm.py
python metrics.py
python chatbot.py
```
---

## Author

Kall-K

---

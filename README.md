# Agentic Automation Platform (Free APIs + Ollama)

A lightweight agentic workflow system in Python demonstrating:
- multi-step agent loop (decide → tool call → observe → iterate)
- tool-based API catalog discovery/selection
- real HTTP calls to a free/no-auth API (Exchangerate Host)
- structured JSON outputs validated by Pydantic
- trace logging to JSONL for debugging

## Free API used (from the Public APIs ecosystem)
- **Exchangerate Host** (no-auth) for live FX rates.

Catalog also includes key-based APIs (IPstack, Weatherstack, Fixer, etc.) to demonstrate auth gating and extensibility.

## Requirements
- Python 3.11+
- [Ollama](https://ollama.com/) installed and running

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
ollama pull llama3.1:8b

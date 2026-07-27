# GemmaTalks

> **Status:** Local prototype. Public sharing is optional and requires network access.

GemmaTalks sends chat messages to a Gemma model served by Ollama and streams the response through a Gradio interface. Model inference runs on the local Ollama service and does not require a hosted LLM API.

Local mode binds to `127.0.0.1` and does not create a public Gradio link. Setting `GRADIO_SHARE=true` exposes the locally running interface through Gradio's public-share mechanism and therefore requires an internet connection.

## Requirements

- Python 3.10 or later
- Ollama installed and running
- A compatible Gemma model available in Ollama

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
ollama pull gemma3
python app.py
```

Open `http://127.0.0.1:7860`.

## Configuration

Copy `.env.example` values into your shell or local environment manager.

| Variable | Default | Purpose |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Ollama service URL |
| `OLLAMA_MODEL` | `gemma3` | Ollama model name |
| `CONNECT_TIMEOUT_SECONDS` | `5` | Connection timeout |
| `READ_TIMEOUT_SECONDS` | `180` | Streaming read timeout |
| `GRADIO_HOST` | `127.0.0.1` | Local bind address |
| `GRADIO_PORT` | `7860` | Local port |
| `GRADIO_SHARE` | `false` | Explicitly enable optional public sharing |

## Test

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
```

Tests mock Ollama; they do not download a model or create a public share URL.

## Privacy and network boundary

- Local inference avoids a hosted model API.
- Prompts and responses travel between the browser, Gradio process, and local Ollama service.
- Enabling public sharing routes browser access through a public network endpoint.
- This is a prototype and is not an authenticated multi-user service.

## Limitations

- No durable chat history
- No authentication or authorization
- No retrieval-augmented generation in this repository
- Model quality and hardware requirements depend on the selected Ollama model

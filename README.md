# RemoteAI

RemoteAI is a lightweight local personal assistant. The browser UI, API, conversation memory and agent orchestration run locally; Google Colab hosts model inference.

## Multi-agent layout
- Coordinator: decomposes a multi-part request into at most three subtasks and synthesises results.
- Specialists: Research, Developer, Planner, Writer, Analyst and General.
- Concurrent execution is bounded by `AGENT_MAX_PARALLEL` (default 3).
- Specialists currently share one Colab model endpoint and use different role prompts. They are not separate model instances.

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload
```
Open http://127.0.0.1:8000 and configure your active Colab tunnel URL.

## Colab API contract
The adapter currently expects an OpenAI-compatible API:
- POST `/v1/chat/completions`
- Request JSON: `model`, `messages`, `temperature`
- Response JSON: `choices[0].message.content`
- Optional GET `/health`

The exact contract must be checked against your Colab notebook. A different endpoint or response schema requires a small adapter change in `app/providers/colab.py`.

## Local configuration
The URL/model are stored in `data/config.json` (ignored by Git). Keep API keys in local `.env`; never commit tunnel URLs or credentials. Colab tunnel URLs are temporary and must be refreshed after a runtime restart.

## API
- `GET /api/health`
- `GET /api/provider/config`, `GET /api/provider/health`
- `PUT /api/provider/colab`
- `POST /api/chat`
- `GET/POST /api/memory/facts`, `GET/POST /api/memory/tasks`

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

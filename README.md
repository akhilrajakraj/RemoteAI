# RemoteAI

A modular, permission-aware personal AI assistant with a FastAPI backend and a lightweight web HUD.

## Structure
- `app/config.py` — environment-based runtime configuration
- `app/memory.py` — SQLite conversations, facts, tasks, and audit events
- `app/brain.py` — assistant orchestration
- `app/providers/` — local Ollama and optional remote model providers
- `app/tools/` — capability modules for desktop, developer, and personal workflows
- `app/api/` — FastAPI routes
- `static/index.html` — pink assistant interface
- `main.py` — FastAPI entry point
- `scaffold.py` — project directory bootstrap helper
- `docs/ROADMAP.md` — staged implementation plan

## Principles
Start as a modular monolith: lightweight to run locally, easy to extend, and explicit about permissions. Ollama is the default provider; an optional remote endpoint can be configured.

## Safety
Tool execution is not enabled by default. Add narrowly scoped, allow-listed tools and require user approval for destructive actions and external side effects. Never expose unrestricted shell or desktop control.

## Quick start
1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and adjust settings if needed.
4. Start Ollama and pull the configured model, or configure the remote provider.
5. Run `uvicorn main:app --reload` and open `http://127.0.0.1:8000`.

See `docs/ROADMAP.md` for the next milestones.

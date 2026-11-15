# RemoteAI

A modular, permission-aware personal AI assistant with a FastAPI backend and a lightweight web HUD.

## Current scaffold

- `app/config.py` — environment and persisted runtime configuration.
- `app/memory.py` — SQLite-backed conversations, facts, tasks, and audit events.
- `app/brain.py` — async orchestration and tool execution loop.
- `app/tools/` — capability modules for desktop, developer, and personal workflows.
- `static/index.html` — pink Nova-inspired assistant interface.
- `main.py` — FastAPI application entry point.
- `scaffold.py` — local project bootstrap helper.

## Design principles

RemoteAI starts as a modular monolith: simple to run locally, easy to extend, and explicit about permissions. Model access is provider-based so local Ollama can be used first, with optional remote endpoints such as a Colab-hosted model.

## Safety

Tool execution is allow-listed. Destructive actions and external side effects must require explicit user confirmation. Do not expose an unrestricted shell or desktop-control endpoint.

## Status

Initial repository scaffold. See `docs/ROADMAP.md` for the staged implementation plan.

# RemoteAI Roadmap

## Phase 1 — Stable foundation
- FastAPI application and health endpoint
- SQLite persistence for conversations, facts, tasks, and audit events
- Provider interface with local Ollama and optional remote endpoint
- Basic chat interface

## Phase 2 — Brain and tools
- Explicit tool registry with JSON schemas
- Tool input validation and permission scopes
- Approval flow for file changes, commands, and external side effects
- Bounded tool-call loop with timeouts and audit records

## Phase 3 — Memory
- Conversation summaries and user-approved long-term facts
- Memory retrieval with source and timestamp metadata
- User controls to inspect, edit, and delete stored memories

## Phase 4 — Capabilities
- Developer workflow tools
- Personal productivity tools
- Carefully scoped desktop integrations
- Background jobs only when a demonstrated use case requires them

## Phase 5 — Product quality
- Authentication for remote access
- Secure secrets management
- Tests, structured logging, backups, and deployment documentation

## Architecture constraints
Start as a modular monolith. Keep local-first operation viable on modest hardware.
Do not add microservices, Redis, a vector database, or unrestricted computer control
until a demonstrated requirement justifies them.

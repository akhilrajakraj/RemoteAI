# RemoteAI architecture

Browser UI -> Local FastAPI -> Coordinator -> specialist agents -> ColabProvider -> Google Colab model server/tunnel.

## Ownership
The local application owns HTTP APIs, UI, SQLite conversation history, agent routing, bounded concurrency and runtime configuration. Colab is responsible only for model inference. Losing the Colab session should produce a provider error, not erase local conversation data.

## Agent lifecycle
1. Coordinator asks the model to split only explicitly multi-part requests into at most three independent tasks.
2. Each task is assigned a specialist role.
3. Tasks run concurrently behind an asyncio semaphore (default maximum three).
4. The coordinator synthesises multiple outputs into one response.
5. The conversation is saved locally.

All roles currently share the same underlying model. This is a role-based multi-agent workflow, not independent model processes. Every request currently incurs a planning call plus one or more execution calls; multi-agent requests add a synthesis call.

## Colab contract
The initial adapter expects POST `/v1/chat/completions` with an OpenAI-compatible `messages` array and a response containing `choices[0].message.content`. Optional health check probes `/health` and `/`. Align this adapter with the actual notebook before treating the integration as verified.

## Scaling path
- Keep local inference optional and lightweight.
- Keep concurrency capped to protect Colab GPU/RAM quotas.
- Add request IDs, structured logs, retries with backoff and cancellation.
- For multi-user deployment, add authentication, per-user isolation, rate limits and PostgreSQL.
- Add Redis/Celery or another durable queue only for long-running background jobs.
- Add tracing/metrics and per-user quotas before public deployment.

## Security boundary
Do not expose the local server publicly without authentication. Treat the Colab tunnel as an exposed endpoint; use authentication where supported. No unrestricted shell, filesystem or desktop execution is enabled.

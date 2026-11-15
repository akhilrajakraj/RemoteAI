# RemoteAI architecture

Browser -> local FastAPI -> coordinator -> specialist roles -> Colab Ollama provider -> Cloudflare Quick Tunnel -> Ollama in Google Colab -> Qwen 3.5 9B.

## Notebook-derived integration
The uploaded notebook installs Ollama and cloudflared, sets Ollama to listen on port 11434, starts `ollama serve`, pulls `qwen3.5:9b`, and exposes `http://localhost:11434` via `cloudflared tunnel --url`. The public URL is a temporary trycloudflare.com URL.

The provider uses:
- `GET /api/tags` to check the tunnel and enumerate models.
- `POST /api/chat` with `model`, `messages`, and `stream:false`.
- `message.content` as the response.

## Agent execution
The coordinator may split an explicitly multi-part request into up to three subtasks. Specialist roles share one underlying model. Async tasks are bounded by a semaphore. Multiple subtasks require multiple inference calls plus a synthesis call, so concurrency is deliberately capped.

## Scaling
Start with this modular monolith. For actual multi-user deployment, add authentication, user-isolated conversations, rate limits, request IDs, structured logs, retries/backoff, cancellation, and PostgreSQL. Add Redis and durable workers only when there is a need for background jobs or multiple app instances. A single Colab GPU is a bottleneck, not an elastic inference cluster; increasing agent concurrency does not increase GPU capacity.

## Security warning
The notebook's Quick Tunnel exposes Ollama's HTTP API. The notebook does not show an auth layer. Treat the URL as a public bearer secret and avoid sensitive content. For production, put an authenticated gateway in front of Ollama and protect the local app API.

# RemoteAI

A lightweight local multi-agent assistant. The UI, API, memory and orchestration run on your computer; Google Colab runs Ollama and the Qwen model.

## Your Colab setup
The supplied `RemoteAi.ipynb` installs Ollama, starts it on port 11434, pulls `qwen3.5:9b`, and exposes that port using a Cloudflare Quick Tunnel. Copy the printed `https://....trycloudflare.com` URL into RemoteAI.

RemoteAI talks directly to Ollama:
- Health/model list: GET `/api/tags`
- Chat: POST `/api/chat`
- Request: `{"model":"qwen3.5:9b","messages":[...],"stream":false}`
- Response text: `message.content`

No custom FastAPI/Flask server is required inside Colab. The tunnel URL changes when the Colab runtime restarts.

## Local setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn main:app --reload
```
Open http://127.0.0.1:8000, paste the active Cloudflare URL and connect.

## Multi-agent design
Coordinator plus Research, Developer, Planner, Writer, Analyst and General specialist roles. Roles share the same Qwen model endpoint; the coordinator decomposes multi-part work, bounds parallel calls and synthesises results. Default concurrency is 3 to avoid overwhelming the Colab runtime.

## Security and limits
The Cloudflare Quick Tunnel is public. This notebook does not configure authentication on Ollama, so anyone who obtains the URL may be able to call the model. Do not use it for sensitive prompts; use a secured tunnel/authentication proxy before production use. Never commit the live URL or credentials. The local API should remain bound to localhost unless authentication is added.

See [architecture](docs/ARCHITECTURE.md).

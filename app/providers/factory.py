from app.config import Settings
from app.providers.base import ModelProvider
from app.providers.ollama import OllamaProvider
from app.providers.remote import RemoteProvider

def get_provider(settings: Settings) -> ModelProvider:
    if settings.model_provider == "remote":
        if not settings.remote_model_url:
            raise ValueError("REMOTE_MODEL_URL must be configured for remote provider")
        return RemoteProvider(settings.remote_model_url, settings.remote_model_api_key)
    return OllamaProvider(settings.ollama_base_url, settings.ollama_model)

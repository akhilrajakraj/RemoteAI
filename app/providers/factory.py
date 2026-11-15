from app.config import Settings
from app.providers.base import ModelProvider
from app.providers.colab import ColabOllamaProvider
from app.providers.ollama import OllamaProvider

def get_provider(s:Settings)->ModelProvider:
    if s.model_provider.lower()=="ollama":
        return OllamaProvider()
    return ColabOllamaProvider(s.colab_base_url,s.colab_model,s.colab_timeout_seconds,s.colab_api_key)

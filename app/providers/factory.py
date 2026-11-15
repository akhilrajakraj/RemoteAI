from app.config import Settings
from app.providers.base import ModelProvider
from app.providers.colab import ColabProvider
from app.providers.ollama import OllamaProvider
def get_provider(s:Settings)->ModelProvider:
    if s.model_provider.lower()=="ollama": return OllamaProvider()
    return ColabProvider(s.colab_base_url,s.colab_chat_path,s.colab_model,s.colab_api_key,s.colab_timeout_seconds)

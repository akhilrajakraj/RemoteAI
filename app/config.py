import json, os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name:str="RemoteAI"
    environment:str="development"
    host:str="127.0.0.1"
    port:int=8000
    database_url:str="sqlite:///./data/remoteai.db"
    model_provider:str="colab"
    colab_base_url:str=""
    colab_chat_path:str="/v1/chat/completions"
    colab_model:str="remoteai-model"
    colab_api_key:str|None=None
    colab_timeout_seconds:float=120
    agent_max_parallel:int=3
    data_dir:Path=Path("data")
    model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",extra="ignore")

@lru_cache
def get_settings()->Settings:
    settings=Settings()
    path=settings.data_dir/"config.json"
    if path.exists():
        try:
            saved=json.loads(path.read_text(encoding="utf-8"))
            for key in ("colab_base_url","colab_chat_path","colab_model"):
                if saved.get(key) and not os.getenv(key.upper()):
                    setattr(settings,key,saved[key])
        except (OSError,json.JSONDecodeError):
            pass
    return settings

def save_runtime_config(values:dict)->dict:
    settings=get_settings()
    settings.data_dir.mkdir(parents=True,exist_ok=True)
    path=settings.data_dir/"config.json"
    try: current=json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except (OSError,json.JSONDecodeError): current={}
    for key in ("colab_base_url","colab_chat_path","colab_model"):
        if values.get(key) is not None: current[key]=str(values[key]).strip()
    temp=path.with_suffix(".tmp")
    temp.write_text(json.dumps(current,indent=2),encoding="utf-8")
    os.replace(temp,path)
    return current

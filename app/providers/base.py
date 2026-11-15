from abc import ABC,abstractmethod
from typing import Any
class ModelProvider(ABC):
    @abstractmethod
    async def generate(self,messages:list[dict[str,str]],**kwargs:Any)->str: ...
    @abstractmethod
    async def health_check(self)->dict[str,Any]: ...

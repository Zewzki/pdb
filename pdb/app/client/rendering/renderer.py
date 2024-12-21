from abc import ABC, abstractmethod
from typing import Any


class Renderer(ABC):
    @abstractmethod
    def render(self, template: str, context: dict[str, Any]) -> str:
        pass

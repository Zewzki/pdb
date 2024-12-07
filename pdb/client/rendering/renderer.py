from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Renderer(ABC):
    @abstractmethod
    def render(self, template_path: Path, context: dict[str, Any]) -> str:
        pass

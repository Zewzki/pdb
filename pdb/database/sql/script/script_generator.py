from abc import ABC, abstractmethod
from typing import Any


class ScriptGenerator(ABC):
    @abstractmethod
    def generate_script(self, statements: list[str], params: list[list[Any]]) -> str:
        pass

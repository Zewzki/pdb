from abc import ABC, abstractmethod
from typing import Any


class DropGenerator(ABC):
    @abstractmethod
    def generate_drop(self, table: str) -> tuple[str, list[Any]]:
        pass

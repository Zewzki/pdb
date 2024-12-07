from abc import ABC, abstractmethod
from typing import Any


class Importer(ABC):
    @abstractmethod
    def create_import(self, path: str) -> list[list[tuple[str, Any]]]:
        pass

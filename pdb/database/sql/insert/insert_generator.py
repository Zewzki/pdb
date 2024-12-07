from abc import ABC, abstractmethod
from typing import Any


class InsertGenerator(ABC):
    @abstractmethod
    def generate_insert(self, table: str, inserts: list[tuple[str, Any]]) -> tuple[str, list[Any]]:
        pass

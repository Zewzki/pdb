from abc import ABC, abstractmethod
from pdb.database.sql.conditions.condition import ConditionSet
from typing import Any


class DeleteGenerator(ABC):
    @abstractmethod
    def generate_delete(self, table: str, conditions: ConditionSet | None = None) -> tuple[str, list[Any]]:
        pass

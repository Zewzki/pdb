from abc import ABC, abstractmethod
from pdb.database.sql.conditions.condition import ConditionSet
from typing import Any


class UpdateGenerator(ABC):
    @abstractmethod
    def generate_update(
        self,
        table: str,
        puts: list[tuple[str, Any]],
        conditions: ConditionSet | None = None,
    ) -> tuple[str, list[Any]]:
        pass

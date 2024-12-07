from abc import ABC, abstractmethod
from pdb.database.sql.conditions.condition import ConditionSet
from typing import Any


class ConditionGenerator(ABC):
    @abstractmethod
    def generate_conditions(self, conditions: ConditionSet) -> tuple[str, list[Any]]:
        pass

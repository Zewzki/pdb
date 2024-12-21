from abc import ABC, abstractmethod
from pdb.database.models.pdb_column import PdbColumn
from typing import Any


class CreateGenerator(ABC):
    @abstractmethod
    def generate_create(self, table: str, columns: list[PdbColumn]) -> tuple[str, list[Any]]:
        pass

from abc import ABC, abstractmethod
from pdb.database.datatypes.datatypes import PdbDatatype
from typing import Any


class CreateGenerator(ABC):
    @abstractmethod
    def generate_create(self, table: str, columns: list[tuple[str, PdbDatatype, bool]]) -> tuple[str, list[Any]]:
        pass

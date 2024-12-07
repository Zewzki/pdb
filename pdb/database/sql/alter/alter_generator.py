from abc import ABC, abstractmethod
from pdb.database.datatypes.datatypes import PdbDatatype
from typing import Any


class AlterGenerator(ABC):
    @abstractmethod
    def generate_rename_table(self, old_tablename: str, new_tablename: str) -> tuple[str, list[Any]]:
        pass

    @abstractmethod
    def generate_add_column(self, tablename: str, new_col_name: str, dtype: PdbDatatype) -> tuple[str, list[Any]]:
        pass

    @abstractmethod
    def generate_drop_column(self, tablename: str, col_name: str) -> tuple[str, list[Any]]:
        pass

    @abstractmethod
    def generate_rename_column(self, tablename: str, old_col_name: str, new_col_name: str) -> tuple[str, list[Any]]:
        pass

from abc import ABC, abstractmethod
from pdb.database.datatypes.datatypes import PdbDatatype
from typing import Any


class DatatypeConverter(ABC):
    @abstractmethod
    def to_pdb_datatype(self, dtype: Any) -> PdbDatatype:
        pass

    @abstractmethod
    def from_pdb_datatype(self, dtype: PdbDatatype) -> Any:
        pass

from abc import ABC, abstractmethod
from pdb.shared.op_status import OpStatus
from typing import Any


class Exporter(ABC):
    @abstractmethod
    def export(self, col_names: list[str], data: list[list[Any]], output_path: str) -> OpStatus:
        pass

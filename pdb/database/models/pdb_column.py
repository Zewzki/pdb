from pdb.database.datatypes.datatypes import PdbDatatype
from dataclasses import dataclass


@dataclass
class PdbColumn:
    col_name: str
    dtype: PdbDatatype
    is_dropdown: bool = False
    is_unique: bool = False

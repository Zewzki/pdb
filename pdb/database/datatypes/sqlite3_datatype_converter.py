from pdb.database.datatypes.datatype_converter import DatatypeConverter
from pdb.database.datatypes.datatypes import PdbDatatype, Sqlite3Datatype


class Sqlite3DatatypeConverter(DatatypeConverter):
    def from_pdb_datatype(self, dtype: PdbDatatype) -> Sqlite3Datatype:
        match dtype:
            case PdbDatatype.TEXT:
                return Sqlite3Datatype.TEXT
            case PdbDatatype.CHARACTER:
                return Sqlite3Datatype.TEXT
            case PdbDatatype.BOOL:
                return Sqlite3Datatype.INTEGER
            case PdbDatatype.NUMBER:
                return Sqlite3Datatype.INTEGER
            case PdbDatatype.DECIMAL:
                return Sqlite3Datatype.REAL
            case PdbDatatype.DATE:
                return Sqlite3Datatype.TEXT
            case PdbDatatype.TIME:
                return Sqlite3Datatype.TEXT
            case PdbDatatype.TIMESTAMP:
                return Sqlite3Datatype.TEXT
            case PdbDatatype.MONEY:
                return Sqlite3Datatype.TEXT
            case PdbDatatype.RAW:
                return Sqlite3Datatype.BLOB

    def to_pdb_datatype(self, dtype: Sqlite3Datatype) -> PdbDatatype:
        match dtype:
            case Sqlite3Datatype.TEXT:
                return PdbDatatype.TEXT
            case Sqlite3Datatype.NUMERIC:
                return PdbDatatype.NUMBER
            case Sqlite3Datatype.INTEGER:
                return PdbDatatype.NUMBER
            case Sqlite3Datatype.REAL:
                return PdbDatatype.DECIMAL
            case Sqlite3Datatype.BLOB:
                return PdbDatatype.RAW

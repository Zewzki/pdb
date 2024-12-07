from pdb.database.common import SupportedDb
from pdb.database.datatypes.datatype_converter import DatatypeConverter
from pdb.database.datatypes.sqlite3_datatype_converter import Sqlite3DatatypeConverter


class DatatypeConverterFactory:
    @classmethod
    def create_datatype_converter(cls, dbtype: SupportedDb) -> DatatypeConverter:
        match dbtype:
            case SupportedDb.SQLITE3:
                return Sqlite3DatatypeConverter()

from enum import Enum


class PdbDatatype(Enum):
    TEXT = "text"
    CHARACTER = "character"
    NUMBER = "number"
    DECIMAL = "decimal"
    DATE = "date"
    TIME = "time"
    TIMESTAMP = "timestamp"
    BOOL = "bool"
    MONEY = "money"
    RAW = "raw"


class Sqlite3Datatype(Enum):
    TEXT = "TEXT"
    NUMERIC = "NUM"
    INTEGER = "INT"
    REAL = "REAL"
    BLOB = "BLOB"

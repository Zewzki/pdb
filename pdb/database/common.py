from enum import Enum

SQL_NULL = "NULL"
SQL_WILD = "%"


class DebugMode(Enum):
    ENABLED = True
    DISABLED = False


class Status(Enum):
    FAIL = False
    SUCCESS = True


class DbStatus:
    def __init__(self, status: Status, msg: str) -> None:
        self.status = status
        self.msg = msg


class OrderDir(Enum):
    ASC = "ASC"
    DESC = "DESC"


class SupportedDb(Enum):
    PSYCOPG2 = "psycopg2"
    SQLITE3 = "sqlite3"
    PYMSSQL = "pymssql"


class QueryPlaceholder(Enum):
    QMARK = "?"
    PCENT = "%s"
    NA = ""


class JoinType(Enum):
    INNER = "INNER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    FULL = "FULL"


class SqlLogicalOp(Enum):
    AND = "AND"
    OR = "OR"


class SqlOp(Enum):
    EQ = "="
    NE = "!="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    LTGT = "<>"

    ALL = "ALL"
    AND = "AND"
    ANY = "ANY"
    BETWEEN = "BETWEEN"
    EXISTS = "EXISTS"
    IS = "IS"
    IN = "IN"
    NOT = "NOT"
    LIKE = "LIKE"
    ILIKE = "ILIKE"
    OR = "OR"


class QueryModifier(Enum):
    CI = "ci"
    CS = "cs"


class SqlFunction(Enum):
    DISTINCT = "DISTINCT({value})"
    COUNT = "COUNT({value})"
    UPPER = "UPPER({value})"
    LOWER = "LOWER({value})"


class Missing:
    pass

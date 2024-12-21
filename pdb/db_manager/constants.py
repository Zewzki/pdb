from pdb.database.models.pdb_column import PdbColumn
from pdb.database.datatypes.datatypes import PdbDatatype

COL_TABLENAME = "tablename"
COL_COLNAME = "col_name"
COL_DATATYPE = "datatype"
COL_ISDROP = "is_dropdown"
COL_ISUNIQUE = "is_unique"
COL_VAL = "value"
COL_USERNAME = "username"
COL_ROLE = "role"
COL_PW_SALT = "pw_salt"
COL_PW_HASH = "pw_hash"
COL_PW_ALGO = "pw_algo"
COL_SESS_TOKEN = "session_token"
COL_EXP = "expiration"
COL_CAN_READ = "can_read"
COL_CAN_WRITE = "can_write"
COL_ROWID = "ROWID"


TABLE_METADATA = "table_metadata"
TABLE_DROPDOWNS = "dropdowns"
TABLE_AUTH = "auth"
TABLE_SESS = "sessions"
TABLE_PERMS = "table_permissions"

METADATA_COLUMNS = [
    PdbColumn(COL_TABLENAME, PdbDatatype.TEXT, is_unique=True),
    PdbColumn(COL_COLNAME, PdbDatatype.TEXT, is_unique=True),
    PdbColumn(COL_DATATYPE, PdbDatatype.TEXT),
    PdbColumn(COL_ISDROP, PdbDatatype.BOOL),
    PdbColumn(COL_ISUNIQUE, PdbDatatype.BOOL),
]

DROPDOWNS_COLUMNS = [
    PdbColumn(COL_TABLENAME, PdbDatatype.TEXT, is_unique=True),
    PdbColumn(COL_COLNAME, PdbDatatype.TEXT, is_unique=True),
    PdbColumn(COL_VAL, PdbDatatype.TEXT, is_unique=True),
]

AUTH_COLUMNS = [
    PdbColumn(COL_USERNAME, PdbDatatype.TEXT, is_unique=True),
    PdbColumn(COL_ROLE, PdbDatatype.TEXT),
    PdbColumn(COL_PW_SALT, PdbDatatype.TEXT),
    PdbColumn(COL_PW_HASH, PdbDatatype.RAW),
    PdbColumn(COL_PW_ALGO, PdbDatatype.TEXT),
]

SESSION_COLUMNS = [
    PdbColumn(COL_USERNAME, PdbDatatype.TEXT, is_unique=True),
    PdbColumn(COL_SESS_TOKEN, PdbDatatype.RAW),
    PdbColumn(COL_EXP, PdbDatatype.TIMESTAMP),
]

PERMS_COLUMNS = [
    PdbColumn(COL_TABLENAME, PdbDatatype.TEXT, is_unique=True),
    PdbColumn(COL_USERNAME, PdbDatatype.TEXT, is_unique=True),
    PdbColumn(COL_CAN_READ, PdbDatatype.BOOL),
    PdbColumn(COL_CAN_WRITE, PdbDatatype.BOOL),
]

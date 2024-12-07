from pdb.database.connectors.db_connector import DbConnector
from pdb.database.datatypes.datatypes import PdbDatatype
from pdb.database.sql.conditions.condition import ConditionSet
from pdb.database.sql.sql_collection import SqlCollection
from pdb.shared.constants import SALT_LEN
from pdb.shared.hash.hash_algorithm import HashAlgorithm
from pdb.shared.op_status import OpStatus
from pdb.shared.salt.salter import Salter
from typing import Any, ClassVar


class DbManager2:
    _METADATA_TABLENAME: ClassVar[str] = "table_metadata"
    _METADATA_COLUMNS: ClassVar[list[tuple[str, PdbDatatype]]] = [
        ("tablename", PdbDatatype.TEXT),
        ("col_name", PdbDatatype.TEXT),
        ("datatype", PdbDatatype.TEXT),
        ("is_dropdown", PdbDatatype.BOOL),
    ]

    _DROPDOWNS_TABLENAME: ClassVar[str] = "dropdowns"
    _DROPDOWNS_COLUMNS: ClassVar[list[tuple[str, PdbDatatype]]] = [
        ("tablename", PdbDatatype.TEXT),
        ("col_name", PdbDatatype.TEXT),
        ("value", PdbDatatype.TEXT),
    ]

    _AUTH_TABLENAME: ClassVar[str] = "auth"
    _AUTH_COLUMNS: ClassVar[list[tuple[str, PdbDatatype]]] = [
        ("username", PdbDatatype.TEXT),
        ("role", PdbDatatype.TEXT),
        ("pw_salt", PdbDatatype.TEXT),
        ("pw_hash", PdbDatatype.RAW),
        ("pw_algo", PdbDatatype.TEXT),
    ]

    _PERMS_TABLENAME: ClassVar[str] = "table_permissions"
    _PERMS_COLUMNS: ClassVar[list[tuple[str, PdbDatatype]]] = [
        ("tablename", PdbDatatype.TEXT),
        ("username", PdbDatatype.TEXT),
        ("can_read", PdbDatatype.BOOL),
        ("can_write", PdbDatatype.BOOL),
    ]

    def __init__(
        self,
        db: DbConnector,
        sql_collection: SqlCollection,
        hasher: HashAlgorithm,
        salter: Salter,
    ) -> None:
        self._db = db
        self._sql = sql_collection

        self._hasher = hasher
        self._salter = salter

    # Tables

    def initialize_metatables(self) -> OpStatus:
        self._create_table(self._METADATA_TABLENAME, self._METADATA_COLUMNS)
        self._create_table(self._DROPDOWNS_TABLENAME, self._DROPDOWNS_COLUMNS)
        self._create_table(self._AUTH_TABLENAME, self._AUTH_COLUMNS)
        self._create_table(self._PERMS_TABLENAME, self._PERMS_COLUMNS)

    def create_pdb_table(self, tablename: str, columns: list[tuple[str, PdbDatatype, bool]]) -> OpStatus:
        for c in columns:
            meta_inserts = [
                ("tablename", tablename),
                ("col_name", c[0]),
                ("datatype", c[1].value),
                ("is_dropdown", c[2]),
            ]
            self._insert(self._METADATA_TABLENAME, meta_inserts)

        self._create_table(tablename, columns)

    def get_pdb_tables(self) -> list[str]:
        pass

    def remove_pdb_table(self, tablename: str) -> OpStatus:
        self._delete(self._METADATA_COLUMNS, [("tablename", tablename)])
        self._drop(tablename)

    # Table Columns

    def rename_table(self, old_tablename: str, new_tablename: str) -> OpStatus:
        s1 = self._update(
            self._METADATA_TABLENAME,
            puts=[("tablename", new_tablename)],
            conditions=[("tablename", old_tablename)],
        )

        s2 = None
        try:
            sql, params = self._sql.alter_generator.generate_rename_table(old_tablename, new_tablename)
            self._db.write(sql, params)
            s2 = OpStatus(True, f"Renamed table {old_tablename} to {new_tablename}")
        except Exception as ex:
            s2 = OpStatus(False, f"Error renaming table {old_tablename} to {new_tablename}")

        return OpStatus(s1.status and s1.status, f"{s1.msg}\n{s2.msg}")

    def add_table_column(self, tablename: str, column_name: str, dtype: PdbDatatype) -> OpStatus:
        s1 = self._insert(
            self._METADATA_TABLENAME,
            inserts=[
                ("tablename", tablename),
                ("col_name", column_name),
                ("dtype", self._sql.dtype_converter.from_pdb_datatype(dtype)),
            ],
        )

        s2 = None
        try:
            sql, params = self._sql.alter_generator.generate_add_column(tablename, column_name, dtype)
            self._db.write(sql, params)
            s2 = OpStatus(True, f"Added column {column_name} ({dtype.name}) to table {tablename}")
        except Exception as ex:
            s2 = OpStatus(False, f"Error adding column {column_name} ({dtype.name}) to table {tablename}")

        return OpStatus(s1.status and s2.status, f"{s1.msg}\n{s2.msg}")

    def rename_column(self, tablename: str, old_column_name: str, new_column_name: str) -> OpStatus:
        s1 = self._update(
            self._METADATA_TABLENAME,
            puts=[("col_name", new_column_name)],
            conditions=[("tablename", tablename), ("col_name", old_column_name)],
        )

        s2 = None
        try:
            sql, params = self._sql.alter_generator.generate_rename_column(tablename, old_column_name, new_column_name)
            self._db.write(sql, params)
            s2 = OpStatus(True, f"Renamed column {old_column_name} to {new_column_name} on table {tablename}")
        except Exception as ex:
            s2 = OpStatus(False, f"Error renaming column {old_column_name} to {new_column_name} on table {tablename}")

        return OpStatus(s1.status and s2.status, f"{s1.msg}\n{s2.msg}")

    def change_column_type(self, tablename: str, column_name: str, new_type: type) -> OpStatus:
        pass

    def remove_table_column(self, tablename: str, column_name: str) -> OpStatus:
        s1 = self._delete(
            self._METADATA_TABLENAME,
            conditions=[("tablename", tablename), ("col_name", column_name)],
        )
        s2 = None
        try:
            sql, params = self._sql.alter_generator.generate_drop_column(tablename, column_name)
            self._db.write(sql, params)
            s2 = OpStatus(True, f"Column {column_name} removed from table {tablename}")
        except Exception as ex:
            s2 = OpStatus(False, f"Error removing column {column_name} from table {tablename} - {ex}")

        return OpStatus(s1.status and s2.status, f"{s1.msg}\n{s2.msg}")

    # Dropdowns

    def add_dropdown_value(self, tablename: str, column_name: str, value: Any) -> OpStatus:
        return self._insert(
            self._DROPDOWNS_TABLENAME,
            [("tablename", tablename), ("col_name", column_name), ("value", value)],
        )

    def remove_dropdown_value(self, tablename: str, column_name: str, value: Any) -> OpStatus:
        return self._delete(
            self._DROPDOWNS_TABLENAME,
            [("tablename", tablename), ("col_name", column_name), ("value", value)],
        )

    # Users

    def add_user(self, username: str, password: str, role: str) -> OpStatus:
        pw_salt = self._salter.generate_salt(SALT_LEN)
        pw_hash = self._hasher.hash(password, pw_salt)
        return self._insert(
            self._AUTH_TABLENAME,
            [
                ("username", username),
                ("role", role),
                ("pw_hash", pw_hash),
                ("pw_salt", pw_salt),
                ("pw_algo", self._hasher.name),
            ],
        )

    def remove_user(self, username: str) -> OpStatus:
        return self._delete(self._AUTH_TABLENAME, [("username", username)])

    # Perms

    def add_user_permissions(self, tablename: str, username: str, can_read: bool, can_write: bool) -> OpStatus:
        return self._insert(
            self._PERMS_TABLENAME,
            [
                ("tablename", tablename),
                ("username", username),
                ("can_read", can_read),
                ("can_write", can_write),
            ],
        )

    # Table Data

    def get_table(self, tablename: str) -> list[list[Any]]:
        pass

    def add_record(self, tablename: str, record_data: list[tuple[str, Any]]) -> OpStatus:
        return self._insert(tablename, record_data)

    def update_record(self, tablename: str, row_id: int, new_data: list[tuple[str, Any]]) -> OpStatus:
        pass

    def remove_record(self, tablename: str, row_id: int) -> OpStatus:
        pass

    # Internal

    def _create_table(self, tablename: str, columns: list[tuple[str, PdbDatatype, bool]]) -> OpStatus:
        try:
            sql, params = self._sql.create_generator.generate_create(tablename, columns)
            self._db.write(sql, params)
        except Exception as ex:
            return OpStatus(False, f"Error creating table {tablename}")
        return OpStatus(True, f"Table {tablename} created...")

    def _query(self, tablename: str) -> OpStatus:
        pass

    def _insert(self, tablename: str, inserts: list[tuple[str, Any]]) -> OpStatus:
        try:
            sql, params = self._sql.insert_generator.generate_insert(tablename, inserts)
            self._db.write(sql, params)
        except Exception as ex:
            return OpStatus(False, f"Error inserting to table {tablename}: {inserts} - {ex}")
        return OpStatus(True, f"Insert to table {tablename} complete...")

    def _update(self, tablename: str, puts: list[tuple[str, Any]], conditions: ConditionSet | None = None) -> OpStatus:
        try:
            sql, params = self._sql.update_generator.generate_update(tablename, puts, conditions)
            self._db.write(sql, params)
        except Exception as ex:
            return OpStatus(False, f"Error updating table {tablename} with {puts} where {conditions} - {ex}")
        return OpStatus(True, f"Update to table {tablename} complete...")

    def _delete(self, tablename: str, conditions: ConditionSet | None = None) -> OpStatus:
        try:
            sql, params = self._sql.delete_generator.generate_delete(tablename, conditions)
            self._db.write(sql, params)
        except Exception as ex:
            return OpStatus(False, f"Error deleting from table {tablename} where {conditions} - {ex}")
        return OpStatus(True, f"Deletetion from table {tablename} complete...")

    def _drop(self, tablename: str) -> OpStatus:
        try:
            sql, _ = self._sql.drop_generator.generate_drop(tablename)
            self._db.write(sql)
        except Exception as ex:
            return OpStatus(False, f"Error dropping table {tablename} - {ex}")
        return OpStatus(True, f"Table {tablename} drop complete...")

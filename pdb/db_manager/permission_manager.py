from pdb.database.connectors.db_connector import DbConnector
from pdb.database.sql.sql_collection import SqlCollection
from pdb.shared.op_status import OpStatus
from pdb.db_manager.constants import TABLE_PERMS, COL_USERNAME, COL_TABLENAME, COL_CAN_READ, COL_CAN_WRITE


class PermissionManager:
    def __init__(self, db: DbConnector, sql: SqlCollection) -> None:
        self._db = db
        self._sql = sql

    def get_user_permissions(self, username: str) -> OpStatus:
        sql, params = self._sql.query_generator.create_query(
            TABLE_PERMS, return_fields=[COL_TABLENAME, COL_CAN_READ, COL_CAN_WRITE], conditions=[(COL_USERNAME, username)]
        )

        try:
            results = self._db.read(sql, params)
            if results is None or len(results) <= 0:
                return OpStatus(False, f"No")

            return OpStatus(True, results)

        except Exception as ex:
            return OpStatus(False, f"Error fetching user permissions...")

    def check_user_table_permissions(self, tablename: str, username: str) -> OpStatus:
        sql, params = self._sql.query_generator.create_query(
            TABLE_PERMS, return_fields=[COL_CAN_READ, COL_CAN_WRITE], conditions=[(COL_USERNAME, username), (COL_TABLENAME, tablename)]
        )

        try:
            results = self._db.read(sql, params)
            if results is None or len(results) <= 0:
                return OpStatus(False, f"No")

            perms_entry = results[0]

            return OpStatus(True, (perms_entry[0], perms_entry[1]))

        except Exception as ex:
            return OpStatus(False, f"Error fetching user permissions...")

    def add_user_permissions(self, tablename: str, username: str, can_read: bool, can_write: bool) -> OpStatus:
        sql, params = self._sql.insert_generator.generate_insert(
            TABLE_PERMS,
            [
                (COL_TABLENAME, tablename),
                (COL_USERNAME, username),
                (COL_CAN_READ, can_read),
                (COL_CAN_WRITE, can_write),
            ],
        )

        try:
            self._db.write(sql, params)
            return OpStatus(True, f"User permissions added...")
        except Exception as ex:
            return OpStatus(False, f"Error adding user permission for {username} - {ex}")

    def update_user_permissions(self, tablename: str, username: str, can_read: bool, can_write: bool) -> OpStatus:
        sql, params = self._sql.update_generator.generate_update(
            TABLE_PERMS,
            [
                (COL_TABLENAME, tablename),
                (COL_USERNAME, username),
                (COL_CAN_READ, can_read),
                (COL_CAN_WRITE, can_write),
            ],
            [
                (COL_TABLENAME, tablename),
                (COL_USERNAME, username),
            ],
        )

        try:
            self._db.write(sql, params)
            return OpStatus(True, f"User permissions updated...")
        except Exception as ex:
            return OpStatus(False, f"Error updating user permission for {username} - {ex}")

    def remove_user_permissions(self, tablename: str, username: str) -> OpStatus:
        sql, params = self._sql.delete_generator.generate_delete(TABLE_PERMS, conditions=[(COL_TABLENAME, tablename), (COL_USERNAME, username)])
        try:
            self._db.write(sql, params)
            return OpStatus(True, f"User permission removed...")
        except Exception as ex:
            return OpStatus(False, f"Error removing user permission for {username} - {ex}")

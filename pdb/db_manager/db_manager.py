from datetime import timedelta
from pdb.database.connectors.db_connector import DbConnector
from pdb.database.sql.sql_collection import SqlCollection
from pdb.db_manager.auth_manager import AuthManager
from pdb.db_manager.dropdown_manager import DropdownManager
from pdb.db_manager.metatable_manager import MetaTableManager
from pdb.db_manager.permission_manager import PermissionManager
from pdb.db_manager.session_manager import SessionManager
from pdb.db_manager.user_table_manager import UserTableManager
from pdb.shared.hash.hash_algorithm import HashAlgorithm
from pdb.shared.salt.salter import Salter


class DbManager:
    def __init__(
        self,
        db: DbConnector,
        sql_collection: SqlCollection,
        hasher: HashAlgorithm,
        salter: Salter,
        session_timeout: timedelta,
    ) -> None:
        self._db = db
        self._sql = sql_collection

        self.meta_table_manager = MetaTableManager(db, sql_collection)
        self.auth_manager = AuthManager(db, sql_collection, hasher, salter)
        self.session_manager = SessionManager(db, sql_collection, session_timeout)
        self.dropdown_manager = DropdownManager(db, sql_collection)
        self.permission_manager = PermissionManager(db, sql_collection)
        self.user_table_manager = UserTableManager(db, sql_collection)

        self.meta_table_manager.initialize_internal_tables()

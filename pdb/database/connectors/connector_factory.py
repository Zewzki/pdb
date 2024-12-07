from pdb.database.common import SupportedDb
from pdb.database.config.db_config import DbConfig
from pdb.database.connectors.db_connector import DbConnector
from pdb.database.connectors.psycopg2_connector import Psycopg2Connector
from pdb.database.connectors.sqlite3_connector import Sqlite3Connector


class ConnectorFactory:
    @classmethod
    def create_connector(cls, dbtype: SupportedDb, db_config: DbConfig) -> DbConnector:
        match dbtype:
            case SupportedDb.PYMSSQL:
                pass
            case SupportedDb.PSYCOPG2:
                return Psycopg2Connector(db_config)
            case SupportedDb.SQLITE3:
                return Sqlite3Connector(db_config)

        return None

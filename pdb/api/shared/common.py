from pdb.api.shared.constants import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_TYPE, DB_USER, HASH_TYPE, SALT_TYPE
from pdb.database.config.db_config import DbConfig
from pdb.database.connectors.connector_factory import ConnectorFactory
from pdb.database.datatypes.datatype_converter_factory import DatatypeConverterFactory
from pdb.database.sql.sql_collection import SqlCollection
from pdb.database.sql.sql_factory import SqlFactory
from pdb.db_manager.db_manager import DbManager
from pdb.shared.hash.hasher_factory import HasherFactory
from pdb.shared.salt.salt_factory import SaltFactory

db_config = DbConfig(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
db = ConnectorFactory.create_connector(DB_TYPE)
sql_collection = SqlCollection(
    DatatypeConverterFactory.create_datatype_converter(DB_TYPE),
    SqlFactory.create_create_generator(DB_TYPE),
    SqlFactory.create_query_generator(DB_TYPE),
    SqlFactory.create_insert_generator(DB_TYPE),
    SqlFactory.create_update_generator(DB_TYPE),
    SqlFactory.create_delete_generator(DB_TYPE),
    SqlFactory.create_drop_generator(DB_TYPE),
    SqlFactory.create_alter_generator(DB_TYPE),
)
hasher = HasherFactory.create_hasher(HASH_TYPE)
salter = SaltFactory.create_salter(SALT_TYPE)
db_manager = DbManager(db, sql_collection, hasher, salter)

from pdb.database.common import QueryPlaceholder, SupportedDb
from pdb.database.datatypes.sqlite3_datatype_converter import Sqlite3DatatypeConverter
from pdb.database.sql.alter.alter_generator import AlterGenerator
from pdb.database.sql.alter.standard_alter_generator import StandardAlterGenerator
from pdb.database.sql.conditions.condition_generator import ConditionGenerator
from pdb.database.sql.conditions.standard_condition_generator import StandardConditionGenerator
from pdb.database.sql.create.create_generator import CreateGenerator
from pdb.database.sql.create.standard_create_generator import StandardCreateGenerator
from pdb.database.sql.delete.delete_generator import DeleteGenerator
from pdb.database.sql.delete.standard_delete_generator import StandardDeleteGenerator
from pdb.database.sql.drop.drop_generator import DropGenerator
from pdb.database.sql.drop.standard_drop_generator import StandardDropGenerator
from pdb.database.sql.insert.insert_generator import InsertGenerator
from pdb.database.sql.insert.standard_insert_generator import StandardInsertGenerator
from pdb.database.sql.query.query_generator import QueryGenerator
from pdb.database.sql.query.sqlite3_query_generator import Sqlite3QueryGenerator
from pdb.database.sql.update.standard_update_generator import StandardUpdateGenerator
from pdb.database.sql.update.update_generator import UpdateGenerator
from pdb.database.sql.script.script_generator import ScriptGenerator
from pdb.database.sql.script.standard_script_generator import StandardScriptGenerator


class SqlFactory:
    @classmethod
    def create_create_generator(cls, dbtype: SupportedDb) -> CreateGenerator:
        match dbtype:
            case SupportedDb.SQLITE3:
                return StandardCreateGenerator(Sqlite3DatatypeConverter())

    @classmethod
    def create_query_generator(cls, dbtype: SupportedDb) -> QueryGenerator:
        match dbtype:
            case SupportedDb.SQLITE3:
                return Sqlite3QueryGenerator(QueryPlaceholder.QMARK)

    @classmethod
    def create_insert_generator(cls, dbtype: SupportedDb) -> InsertGenerator:
        match dbtype:
            case SupportedDb.SQLITE3:
                return StandardInsertGenerator(QueryPlaceholder.QMARK)

    @classmethod
    def create_update_generator(cls, dbtype: SupportedDb) -> UpdateGenerator:
        match dbtype:
            case SupportedDb.SQLITE3:
                return StandardUpdateGenerator(QueryPlaceholder.QMARK)

    @classmethod
    def create_delete_generator(cls, dbtype: SupportedDb) -> DeleteGenerator:
        match dbtype:
            case SupportedDb.SQLITE3:
                return StandardDeleteGenerator(QueryPlaceholder.QMARK)

    @classmethod
    def create_condition_generator(cls, dbtype: SupportedDb) -> ConditionGenerator:
        match dbtype:
            case SupportedDb.SQLITE3:
                return StandardConditionGenerator(QueryPlaceholder.QMARK)

    @classmethod
    def create_drop_generator(cls, dbtype: SupportedDb) -> DropGenerator:
        match dbtype:
            case SupportedDb.SQLITE3:
                return StandardDropGenerator()

    @classmethod
    def create_alter_generator(cls, dbtype: SupportedDb) -> AlterGenerator:
        match dbtype:
            case SupportedDb.SQLITE3:
                return StandardAlterGenerator(Sqlite3DatatypeConverter())

    @classmethod
    def create_script_generator(cls, dbtype: SupportedDb, query_placeholder: QueryPlaceholder) -> ScriptGenerator:
        match dbtype:
            case SupportedDb.SQLITE3:
                return StandardScriptGenerator(query_placeholder)

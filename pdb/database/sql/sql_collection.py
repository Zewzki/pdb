from pdb.database.datatypes.datatype_converter import DatatypeConverter
from pdb.database.sql.alter.alter_generator import AlterGenerator
from pdb.database.sql.create.create_generator import CreateGenerator
from pdb.database.sql.delete.delete_generator import DeleteGenerator
from pdb.database.sql.drop.drop_generator import DropGenerator
from pdb.database.sql.insert.insert_generator import InsertGenerator
from pdb.database.sql.query.query_generator import QueryGenerator
from pdb.database.sql.update.update_generator import UpdateGenerator
from pdb.database.sql.script.script_generator import ScriptGenerator


class SqlCollection:
    def __init__(
        self,
        dtype_converter: DatatypeConverter,
        create_generator: CreateGenerator,
        query_generator: QueryGenerator,
        insert_generator: InsertGenerator,
        update_generator: UpdateGenerator,
        delete_generator: DeleteGenerator,
        drop_generator: DropGenerator,
        alter_generator: AlterGenerator,
        script_generator: ScriptGenerator,
    ) -> None:
        self._conv = dtype_converter
        self._cg = create_generator
        self._qg = query_generator
        self._ig = insert_generator
        self._ug = update_generator
        self._dg = delete_generator
        self._drop_g = drop_generator
        self._ag = alter_generator
        self._sg = script_generator

    @property
    def dtype_converter(self) -> DatatypeConverter:
        return self._conv

    @property
    def create_generator(self) -> CreateGenerator:
        return self._cg

    @property
    def query_generator(self) -> QueryGenerator:
        return self._qg

    @property
    def insert_generator(self) -> InsertGenerator:
        return self._ig

    @property
    def update_generator(self) -> UpdateGenerator:
        return self._ug

    @property
    def delete_generator(self) -> DeleteGenerator:
        return self._dg

    @property
    def drop_generator(self) -> DropGenerator:
        return self._drop_g

    @property
    def alter_generator(self) -> AlterGenerator:
        return self._ag

    @property
    def script_generator(self) -> ScriptGenerator:
        return self._sg

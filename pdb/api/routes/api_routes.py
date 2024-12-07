from fastapi import APIRouter, Request, Response

pdb_routes = APIRouter()


@pdb_routes.post("/auth")
def authenticate(req: Request) -> Response:
    pass


@pdb_routes.get("/users")
def users(req: Request) -> Response:
    pass


@pdb_routes.get("/tables")
def all_tables(req: Request) -> Response:
    pass


@pdb_routes.get("/login")
def login(req: Request) -> Response:
    pass


@pdb_routes.get("/tables/{tablename}")
def get_table(req: Request) -> Response:
    pass


@pdb_routes.get("/")
def home(req: Request) -> Response:
    pass

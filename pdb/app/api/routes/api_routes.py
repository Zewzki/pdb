from fastapi import APIRouter, Request, Response, JSONResponse
from pdb.app.shared.common import db_manager

api_routes = APIRouter()

@api_routes.post("/auth")
def authenticate(req: Request) -> Response:
    pass

@api_routes.post("/create-table")
def create_table(req: Request) -> Response:
    pass

@api_routes.get("/users")
def users(req: Request) -> Response:
    pass


@api_routes.get("/tables")
def all_tables(req: Request) -> Response:
    pass


@api_routes.get("/login")
def login(req: Request) -> Response:
    pass


@api_routes.get("/tables/{tablename}")
def get_table(req: Request, tablename: str) -> Response:
    try:
        return JSONResponse(db_manager.get_pdb_tables())
    except Exception as ex:
        return JSONResponse(f"Error getting table {tablename}")

@api_routes.get("/")
def home(req: Request) -> Response:
    pass

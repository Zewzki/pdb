from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from pdb.app.shared.common import db_manager
from pdb.database.models.pdb_column import PdbColumn

meta_routes = APIRouter()


@meta_routes.post("/add-table")
async def create_table(req: Request, tablename: str, columns: list[PdbColumn]) -> JSONResponse:
    try:
        status = db_manager.meta_table_manager.add_table(tablename, columns)
        if not status.status:
            return JSONResponse({"response": f"Error creating table - {status.content}"}, status_code=502)
    except Exception as ex:
        return JSONResponse({"response": f"Error creating table - {ex}"}, status_code=502)
    return JSONResponse({"response": "Table Created..."})


@meta_routes.put("/rename-table")
async def rename_table(req: Request, old_tablename: str, new_tablename: str) -> JSONResponse:
    try:
        status = db_manager.meta_table_manager.rename_table(old_tablename, new_tablename)
        if not status.status:
            return JSONResponse({"response": f"Error renaming table - {status.content}"}, status_code=502)
    except Exception as ex:
        return JSONResponse({"response": f"Error renaming table - {ex}"}, status_code=502)
    return JSONResponse({"response": "Table Renamed..."})


@meta_routes.post("/add-column")
async def add_column(req: Request, tablename: str, column: PdbColumn) -> JSONResponse:
    try:
        status = db_manager.meta_table_manager.add_table_column(tablename, column)
        if not status.status:
            return JSONResponse({"response": f"Error adding column - {status.content}"}, status_code=502)
    except Exception as ex:
        return JSONResponse({"response": f"Error adding column - {ex}"}, status_code=502)
    return JSONResponse({"response": "Column added..."})


@meta_routes.put("/rename-column")
async def rename_column(req: Request, tablename: str, old_column_name: str, new_column_name: str) -> JSONResponse:
    try:
        status = db_manager.meta_table_manager.rename_column(tablename, old_column_name, new_column_name)
        if not status.status:
            return JSONResponse({"response": f"Error renaming column - {status.content}"}, status_code=502)
    except Exception as ex:
        return JSONResponse({"response": f"Error renaming column - {ex}"}, status_code=502)
    return JSONResponse({"response": "Column renamed..."})


@meta_routes.delete("/remove-column")
async def remove_column(req: Request, tablename: str, column_name: str) -> JSONResponse:
    try:
        status = db_manager.meta_table_manager.remove_table_column(tablename, column_name)
        if not status.status:
            return JSONResponse({"response": f"Error removing column - {status.content}"}, status_code=502)
    except Exception as ex:
        return JSONResponse({"response": f"Error removing column - {ex}"}, status_code=502)
    return JSONResponse({"response": "Column removed..."})


@meta_routes.delete("/remove-table")
async def delete_table(req: Request, tablename: str) -> JSONResponse:
    try:
        status = db_manager.meta_table_manager.remove_table(tablename)
        if not status.status:
            return JSONResponse({"response": f"Error removing table - {status.content}"}, status_code=502)
    except Exception as ex:
        return JSONResponse({"response": f"Error removing table - {ex}"}, status_code=502)
    return JSONResponse({"response": "Table removed..."})

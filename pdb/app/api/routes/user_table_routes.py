from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from pdb.app.shared.common import db_manager
from pdb.database.sql.conditions.condition import ConditionSet
from pdb.database.common import OrderDir, SqlOp

user_table_routes = APIRouter()


@user_table_routes.get("/{tablename}/query")
async def query(
    req: Request,
    tablename: str,
    return_fields: list[str] | None = None,
    conditions: ConditionSet | None = None,
    order_by: str | None = None,
    order_dir: OrderDir = OrderDir.ASC,
    limit: int | None = None,
    offset: int | None = None,
    base_op: SqlOp = SqlOp.AND,
) -> JSONResponse:
    try:
        response = db_manager.user_table_manager.query(
            tablename,
            return_fields,
            conditions,
            order_by,
            order_dir,
            limit,
            offset,
            base_op,
        )
        if not response.status:
            return JSONResponse({"response": f"Could not execute query" - {response.content}}, status_code=502)
        return JSONResponse({"response": response.content})
    except Exception as ex:
        return JSONResponse({"response": f"Error executing query - {ex}"}, status_code=502)


@user_table_routes.post("/{tablename}/insert")
async def add_record(req: Request, tablename: str, inserts: dict[str, Any]) -> JSONResponse:
    try:
        status = db_manager.user_table_manager.add_record(tablename, [(k, v) for k, v in inserts.items()])
        if not status.status:
            return JSONResponse({"response": f"Could not add record - {status.content}"}, status_code=502)
    except Exception as ex:
        return JSONResponse({"response": f"Error adding record - {ex}"}, status_code=502)
    return JSONResponse({"response": f"Record Addedd..."})


@user_table_routes.put("/{tablename}/update")
async def update_record(req: Request, tablename: str, row_id: int, puts: dict[str, Any]) -> JSONResponse:
    try:
        status = db_manager.user_table_manager.update_record(tablename, row_id, [(k, v) for k, v in puts])
        if not status.status:
            return JSONResponse({"response": f"Could not update record - {status.content}"}, status_code=502)
    except Exception as ex:
        return JSONResponse({"response": f"Error updating record - {ex}"}, status_code=502)
    return JSONResponse({"response": f"Record Updated..."})


@user_table_routes.delete("/{tablename}/delete")
async def delete_record(req: Request, tablename: str, row_id: int) -> JSONResponse:
    try:
        status = db_manager.user_table_manager.delete_record(tablename, row_id)
        if not status.status:
            return JSONResponse({"response": f"Could not delete record - {status.content}"}, status_code=502)
    except Exception as ex:
        return JSONResponse({"response": f"Error deleting record - {ex}"}, status_code=502)
    return JSONResponse({"response": f"Record Deleted..."})

from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from pdb.app.shared.common import db_manager

dropdown_routes = APIRouter()


@dropdown_routes.get("/get-dropdowns")
async def get_dropdowns(req: Request, tablename: str, column_name: str) -> JSONResponse:
    try:
        dropdowns = db_manager.dropdown_manager.get_dropdowns(tablename, column_name)
        if not dropdowns.status:
            return JSONResponse({"response": f"Could not fetch dropdowns - {dropdowns.content}"})
        return JSONResponse({"response": dropdowns.content})
    except Exception as ex:
        return JSONResponse({"response": f"Error fetching dropdowns - {ex}"}, status_code=502)


@dropdown_routes.post("/add-dropdown")
async def add_dropdown(req: Request, tablename: str, column_name: str, value: str) -> JSONResponse:
    try:
        status = db_manager.dropdown_manager.add_dropdown_value(tablename, column_name, value)
        if not status.status:
            return JSONResponse({"response": f"Could not add dropdown - {status.content}"})
        return JSONResponse({"response": f"Dropdown added..."})
    except Exception as ex:
        return JSONResponse({"response": f"Error adding dropdown - {ex}"}, status_code=502)


@dropdown_routes.delete("/remove-dropdown")
async def remove_dropdown(req: Request, tablename: str, column_name: str, value: str) -> JSONResponse:
    try:
        status = db_manager.dropdown_manager.remove_dropdown_value(tablename, column_name, value)
        if not status.status:
            return JSONResponse({"response": f"Could not remove dropdown - {status.content}"})
        return JSONResponse({"response": f"Dropdown removed..."})
    except Exception as ex:
        return JSONResponse({"response": f"Error removing dropdown - {ex}"}, status_code=502)

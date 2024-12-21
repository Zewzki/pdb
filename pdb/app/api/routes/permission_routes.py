from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from pdb.app.shared.common import db_manager
from pdb.database.models.pdb_column import PdbColumn

perm_routes = APIRouter()


@perm_routes.post("/add-permission")
async def add_permission(req: Request, tablename: str, username: str, can_read: bool, can_write: bool) -> JSONResponse:
    try:
        status = db_manager.permission_manager.add_user_permissions(tablename, username, can_read, can_write)
        if not status.status:
            return JSONResponse({"response": f"Could not add user permission - {status.content}"}, status_code=502)
        return JSONResponse({"response": f"User Permission Addedd..."})
    except Exception as ex:
        return JSONResponse({"response": f"Error adding user permission - {ex}"}, status_code=502)


@perm_routes.get("/user-perms")
async def get_user_permissions(req: Request, username: str) -> JSONResponse:
    try:
        response = db_manager.permission_manager.get_user_permissions(username)
        if not response.status:
            return JSONResponse({"response": f"Could not fetch user permissions for {username} - {response.content}"}, status_code=502)
        return JSONResponse({"response": response.content})
    except Exception as ex:
        return JSONResponse({"response": f"Error fetching user permission - {ex}"}, status_code=502)


@perm_routes.get("/permit")
async def permit_user(req: Request, tablename: str, username: str) -> JSONResponse:
    try:
        response = db_manager.permission_manager.check_user_table_permissions(tablename, username)
        if not response.status:
            return JSONResponse({"response": f"Could not fetch user table permissions for {username} - {response.content}"}, status_code=502)
        return JSONResponse({"response": response.content})
    except Exception as ex:
        return JSONResponse({"response": f"Error fetch user table permission - {ex}"}, status_code=502)


@perm_routes.put("/update-permission")
async def update_permission(req: Request, tablename: str, username: str, can_read: bool, can_write: bool) -> JSONResponse:
    try:
        status = db_manager.permission_manager.update_user_permissions(tablename, username, can_read, can_write)
        if not status.status:
            return JSONResponse({"response": f"Could not update user permission - {status.content}"}, status_code=502)
        return JSONResponse({"response": f"User Permission Updated..."})
    except Exception as ex:
        return JSONResponse({"response": f"Error update user permission - {ex}"}, status_code=502)


@perm_routes.delete("/remove-permission")
async def remove_permission(req: Request, tablename: str, username: str) -> JSONResponse:
    try:
        status = db_manager.permission_manager.remove_user_permissions(tablename, username)
        if not status.status:
            return JSONResponse({"response": f"Could not remove user permission - {status.content}"}, status_code=502)
        return JSONResponse({"response": f"User Permission Removed..."})
    except Exception as ex:
        return JSONResponse({"response": f"Error removing user permission - {ex}"}, status_code=502)

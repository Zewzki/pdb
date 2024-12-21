from typing import Any

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from pdb.app.shared.common import db_manager
from pdb.shared.constants import SESSION_COOKIE_NAME

auth_routes = APIRouter()


@auth_routes.post("/auth")
async def authenticate(req: Request, username: str, password: str) -> JSONResponse:
    try:
        status = db_manager.auth_manager.authenticate(username, password)
        if not status.status:
            return JSONResponse({"response": status.content}, status_code=401)

        session = db_manager.session_manager.create_session(username)
        if session.status:
            return JSONResponse({"response": "Authenticated"}, headers={"Set-Cookie": f"{SESSION_COOKIE_NAME}={session.content}"})

        return Response({"response": status.content}, status_code=401)
    except Exception as ex:
        return JSONResponse({"response": f"Error during authentication - {ex}"}, status_code=401)


@auth_routes.post("/add-user")
async def add_user(req: Request, username: str, password: str, role: str) -> JSONResponse:
    try:
        status = db_manager.auth_manager.add_user(username, password, role)
        if not status.status:
            return JSONResponse({"response": f"Could not add user {username} - {status.content}"}, status_code=502)
        return JSONResponse({"response": f"User {username} added..."})
    except Exception as ex:
        return JSONResponse({"response": f"Error adding user {username} - {ex}"}, status_code=502)


@auth_routes.delete("/remove-user")
async def remove_user(req: Request, username: str) -> JSONResponse:
    try:
        status = db_manager.auth_manager.remove_user(username)
        if not status.status:
            return JSONResponse({"response": f"Could not remove user {username} - {status.content}"}, status_code=502)
        return JSONResponse({"response": f"User {username} added..."})
    except Exception as ex:
        return JSONResponse({"response": f"Error removing user {username} - {ex}"}, status_code=502)

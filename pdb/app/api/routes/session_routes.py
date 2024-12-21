from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from pdb.app.shared.common import db_manager

session_routes = APIRouter()


@session_routes.post("/verify-session")
async def add_user(req: Request, session_token: str) -> JSONResponse:
    try:
        status = db_manager.session_manager.verify_session(session_token)
        if not status.status:
            return JSONResponse({"response": f"Invalid session token - {status.content}"}, status_code=401)
    except Exception as ex:
        return JSONResponse({"response": f"Error validating session token - {ex}"}, status_code=502)
    return JSONResponse({"response": f"Verified"})

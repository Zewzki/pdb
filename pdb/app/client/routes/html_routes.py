from pdb.app.client.shared.constants import HOME_TEMPLATE
from pdb.app.shared.common import renderer, request_extractor

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

html_routes = APIRouter()


@html_routes.get("/")
def root(req: Request) -> Response:
    data = request_extractor.request_as_dict(req)
    op = renderer.render(HOME_TEMPLATE, data)
    if op.status:
        return HTMLResponse(op.content)
    return HTMLResponse(status_code=502)

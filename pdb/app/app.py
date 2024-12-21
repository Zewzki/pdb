from pdb.app.api.routes.auth_routes import auth_routes
from pdb.app.api.routes.dropdown_routes import dropdown_routes
from pdb.app.api.routes.metatable_routes import meta_routes
from pdb.app.api.routes.permission_routes import perm_routes
from pdb.app.api.routes.session_routes import session_routes
from pdb.app.api.routes.user_table_routes import user_table_routes
from pdb.app.client.routes.html_routes import html_routes

from fastapi import FastAPI

app = FastAPI()
app.include_router(meta_routes, prefix="/api/v1")
app.include_router(auth_routes, prefix="/api/v1")
app.include_router(dropdown_routes, prefix="/api/v1")
app.include_router(perm_routes, prefix="/api/v1")
app.include_router(session_routes, prefix="/api/v1")
app.include_router(user_table_routes, prefix="/api/v1")
app.include_router(user_table_routes, prefix="/api/v1")

app.include_router(html_routes)

from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from app.api.api_v1.routes.user import users_router
from app.api.api_v1.routes.auth import auth_router
from app.api.api_v1.routes.fonction import fonction_router
from app.api.api_v1.routes.ogt import ogt_router
from app.api.api_v1.routes.rubrique import rb_router
from app.api.api_v1.routes.version_ogt import vogt_router
from app.api.api_v1.routes.saisi import router
from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user
#from app.core.celery_app import celery_app
#from app.db.session import init_db
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)
origins = [
    "http://localhost:3000",
    "http://localhost",
    "localhost:3000",
    "localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}

"""
@app.get("/api/v1/task")
async def example_task():
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])

    return {"message": "success"}
"""
#création des tables au démarrage (A retirer si on utilise alembic)
"""
@app.on_event("startup")
def on_startup():
    init_db()
"""


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(fonction_router, prefix="/api/v1", tags=["Fonction"])
app.include_router(ogt_router, prefix="/api/v1", tags=["Ogt"])
app.include_router(rb_router, prefix="/api/v1", tags=["Rubrique"])
app.include_router(vogt_router, prefix="/api/v1", tags=["Versionogt"])
app.include_router(router, prefix="/api/v1", tags=["Saisi"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)


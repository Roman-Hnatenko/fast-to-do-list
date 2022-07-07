from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.access_token.views import auth_router
from api.database import Base, engine
from api.exceptions import HttpUnauthorized
from api.tasks.views import tasks_router
from api.users.views import users_router

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.exception_handler(HttpUnauthorized)
async def unicorn_exception_handler(request: Request, exc: HttpUnauthorized):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=exc.detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(users_router)

from fastapi import FastAPI

from .api.auth import auth_router
from .api.tasks import tasks_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(tasks_router)

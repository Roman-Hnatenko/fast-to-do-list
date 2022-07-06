from typing import Union

from fastapi import APIRouter, status

tasks_router = APIRouter()


@tasks_router.get('/{id}')
async def get_task():
    return 1


@tasks_router.put('/{id}')
async def update_task(item_id: int):
    return {"item_id": item_id}


@tasks_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@tasks_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_task(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@tasks_router.get('/list')
async def get_tasks(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

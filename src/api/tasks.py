from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.exceptions import RecordNotFoundError

from .crud import (delete_task_from_db, get_task_from_db, save_task,
                   update_task_in_db)
from .dependencies import get_current_user, get_db, require_auth
from .models import UserModel
from .schemas import TaskInput, TaskOutput

tasks_router = APIRouter(dependencies=[Depends(require_auth)])


@tasks_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=TaskOutput)
async def create_task(
    task: TaskInput = Body(),
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ddb_task = save_task(db, task, user.id)
    return ddb_task


@tasks_router.get('/{id}', response_model=TaskOutput)
async def get_task(
    id: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        task = get_task_from_db(db, id, user.id)
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task does not exist',
        )
    return task


@tasks_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_task_from_db(db, id, user.id)


# @tasks_router.put('/{id}')
# async def update_task(
#     id: int,
#     user: UserModel = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     update_task_in_db()
#     return {"item_id": item_id}

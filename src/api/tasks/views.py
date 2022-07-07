from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from api.ddb_models import UserModel
from api.dependencies import get_current_user, get_db
from api.exceptions import RecordNotFoundError

from .models import TaskInput, TaskOutput, TaskToUpdate
from .queries import delete_task_from_db, get_task_from_db, save_task, update_task_in_db

tasks_router = APIRouter(prefix='/task')


@tasks_router.post('', status_code=status.HTTP_201_CREATED, response_model=TaskOutput)
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


@tasks_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_task(
    id: int,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_task_from_db(db, id, user.id)


@tasks_router.put('/{id}', response_model=TaskOutput)
async def update_task(
    id: int,
    task: TaskToUpdate = Body(),
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        update_task_in_db(db, id, task, user.id)
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task does not exist',
        )

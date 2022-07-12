from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from api.db_models import UserModel
from api.dependencies import get_current_user, get_session

from .enums import TasksStatus
from .models import TaskInput, TaskOutput, TaskToUpdate
from .queries import delete_task_from_db, get_task_from_db, get_tasks_list, save_task, update_task_in_db

tasks_router = APIRouter(prefix='/task')


@tasks_router.get('/list', response_model=List[TaskOutput])
async def get_tasks(
    user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    tasks_status: TasksStatus = Query(default=TasksStatus.all),
):
    return await get_tasks_list(session, user.id, tasks_status)


@tasks_router.get('/{id}', response_model=TaskOutput)
async def get_task(
    id: int,
    user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        task = await get_task_from_db(session, id, user.id)
    except NoResultFound:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task does not exist',
        )
    return task


@tasks_router.post('', status_code=status.HTTP_201_CREATED, response_model=TaskOutput)
async def create_task(
    task: TaskInput = Body(),
    user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    ddb_task = await save_task(session, task, user.id)
    return ddb_task


@tasks_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_task(
    id: int,
    user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await delete_task_from_db(session, id, user.id)


@tasks_router.put('/{id}', response_model=TaskOutput)
async def update_task(
    id: int,
    task: TaskToUpdate = Body(),
    user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    updated_task = await update_task_in_db(session, id, task, user.id)
    if not updated_task:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task does not exist',
        )
    return updated_task

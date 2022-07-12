from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.db_models import TaskModel

from .enums import TasksStatus
from .models import TaskInput, TaskToUpdate


async def save_task(session: AsyncSession, task: TaskInput, user_id: int) -> TaskModel:
    db_task = TaskModel(**task.dict(), owner_id=user_id)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


async def get_task_from_db(session: AsyncSession, id: int, user_id: int) -> TaskModel:
    result = await session.execute(select(TaskModel).where(TaskModel.id == id, TaskModel.owner_id == user_id))
    return result.scalar_one()


async def delete_task_from_db(session: AsyncSession, id: int, user_id: int):
    query = delete(TaskModel).where(TaskModel.id == id, TaskModel.owner_id == user_id).returning(TaskModel)
    await session.execute(query)
    await session.commit()


async def update_task_in_db(session: AsyncSession, id: int, input_task: TaskToUpdate, user_id: int):
    query = (
        update(TaskModel)
        .where(TaskModel.id == id, TaskModel.owner_id == user_id)
        .values(**input_task.dict(exclude_unset=True))
        .returning(TaskModel)
    )
    task = await session.execute(query)
    await session.commit()
    return task.first()


async def get_tasks_list(session: AsyncSession, user_id: int, tasks_status: TasksStatus):
    filters = [TaskModel.owner_id == user_id]
    if tasks_status == TasksStatus.done:
        filters.append(TaskModel.finished_at.is_not(None))
    elif tasks_status == TasksStatus.in_progress:
        filters.append(TaskModel.finished_at.is_(None))
    result = await session.execute(select(TaskModel).where(*filters))
    return result.scalars().all()

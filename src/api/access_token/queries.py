from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db_models import UserModel


async def get_user(session: AsyncSession, email: str) -> UserModel:
    result = await session.execute(select(UserModel).where(UserModel.email == email))
    return result.scalar_one()

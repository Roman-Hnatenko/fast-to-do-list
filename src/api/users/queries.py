from sqlalchemy.ext.asyncio import AsyncSession

from db_models import UserModel
from api.settings import pwd_context

from .models import UserInput


async def create_user(session: AsyncSession, user: UserInput) -> UserModel:
    db_user = UserModel(
        email=user.email,
        name=user.name,
        hashed_password=pwd_context.hash(user.password),
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

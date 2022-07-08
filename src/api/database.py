import os
from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(os.environ['DATABASE_URL'], echo=True)

async_session_factory = sessionmaker(engine, class_=AsyncSession)
Base = declarative_base()

AsyncScopedSession = async_scoped_session(async_session_factory, scopefunc=current_task)

async_session = AsyncScopedSession()

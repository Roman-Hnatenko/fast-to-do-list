import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(os.environ['DATABASE_URL'], echo=True)

async_session = sessionmaker(engine, class_=AsyncSession)
Base = declarative_base()

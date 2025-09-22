from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.settings.settings import postgres_db_settings as db_set


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{db_set.user}:{db_set.password}@{db_set.host}:{db_set.port}/{db_set.db_name}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()
metadata = Base.metadata

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os

from common import SqlAlchemyBase

load_dotenv()
database_name = os.getenv("DATABASE_NAME")

async_engine = create_async_engine(f"sqlite+aiosqlite:///{database_name}", echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


@asynccontextmanager
async def get_async_alchemy_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except:
            raise


async def create_all_tables_async():
    async with async_engine.begin() as conn:
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine


def create_session(
    database_path: str, echo: bool = False
) -> async_sessionmaker[AsyncSession]:
    async_engine = create_async_engine(database_path, echo=True)

    return async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )


@asynccontextmanager
async def get_async_alchemy_session(
    asyncSessionLocal: async_sessionmaker[AsyncSession],
):
    async with asyncSessionLocal() as session:
        try:
            yield session
        except:
            raise

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from common.database import create_session, get_async_alchemy_session

logger = logging.getLogger(__name__)


class SessionBase:
    _session: AsyncSession
    _database_name: str


def connection(commit: bool = False):
    def con(method):
        async def wrapper(self: SessionBase, *args, **kwargs):
            logger.info(f"Executing {method.__name__} with commit={commit}")
            async with get_async_alchemy_session(
                create_session(self._database_name)
            ) as session:
                self._session = session
                try:
                    result = await method(self, *args, **kwargs)
                    if commit:
                        logger.info(f"Committing transaction for {method.__name__}")
                        await session.commit()
                    logger.info(f"Successfully executed {method.__name__}")
                    return result
                except Exception as exc:
                    logger.error(f"Error in {method.__name__}: {str(exc)}")
                    await session.rollback()
                    raise
                finally:
                    if hasattr(self, "_session"):
                        del self._session

                    await session.close()
                    logger.debug(f"Session closed for {method.__name__}")

        return wrapper

    return con

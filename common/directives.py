from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
import functools


class SessionBase:
    _session: AsyncSession
    async_alchemy_session: async_sessionmaker[AsyncSession]


def connection(commit: bool = False):
    def con(method):
        @functools.wraps
        async def wrapper(self: SessionBase, *args, **kwargs):
            async with self.async_alchemy_session() as session:
                self._session = session
                try:
                    result = await method(self, *args, **kwargs)
                    if commit:
                        await session.commit()
                    return result
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    if hasattr(self, "_session"):
                        del self._session

                    await session.close()

        return wrapper

    return con

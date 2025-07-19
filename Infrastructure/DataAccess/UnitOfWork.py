from typing import Type, TypeVar, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from Infrastructure.DataAccess.Repository import Repository 

T = TypeVar("T")

class UnitOfWork:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self._session: Optional[AsyncSession] = None 

    async def __aenter__(self) -> AsyncSession:
        self._session = self.session_factory()
        await self._session.begin() 
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            if exc_type:
                await self._session.rollback()
            else:
                await self._session.commit()
            await self._session.close()
        self._session = None

    async def get_session(self) -> AsyncSession:
        if not self._session:
            raise RuntimeError("Session not available. Use 'async with UnitOfWork(...)' to initialize.")
        return self._session

    async def get_repository_with_session(self, session: AsyncSession, model: Type[T]) -> Repository[T]:
        return Repository(session, model)

    async def get_repository(self, model: Type[T]) -> Repository[T]:
        return Repository(await self.get_session(), model)

    async def commit(self) -> None:
        if self._session and self._session.in_transaction():
            await self._session.commit()

    async def rollback(self) -> None:
        if self._session and self._session.in_transaction():
            await self._session.rollback()

    async def close_session(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None
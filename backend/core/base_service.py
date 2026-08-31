from typing import TypeVar, Generic, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.logger import logger

T = TypeVar("T")


class BaseService(Generic[T]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def commit_or_rollback(self):
        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            logger.error(f"[BaseService] Database rollback due to exception: {e}")
            raise

"""
Velocity Nexus — Wallet Database Repository
Provides ACID-compliant queries, pagination, caching hooks, and audit logging.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.future import select
from sqlalchemy import update, delete, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import Wallet
from backend.core.logger import logger


class WalletRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, entity_id: str) -> Optional[Wallet]:
        query = select(Wallet).where(Wallet.id == entity_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Wallet]:
        query = select(Wallet).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self) -> int:
        query = select(func.count(Wallet.id))
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def create(self, entity: Wallet) -> Wallet:
        self.db.add(entity)
        await self.db.flush()
        logger.debug(f"[WalletRepository] Created entity with ID {entity.id}")
        return entity

    async def update(self, entity_id: str, update_data: Dict[str, Any]) -> Optional[Wallet]:
        stmt = (
            update(Wallet)
            .where(Wallet.id == entity_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        return await self.get_by_id(entity_id)

    async def delete(self, entity_id: str) -> bool:
        stmt = delete(Wallet).where(Wallet.id == entity_id)
        result = await self.db.execute(stmt)
        return result.rowcount > 0

    async def find_by_criteria(self, filters: Dict[str, Any], limit: int = 50) -> List[Wallet]:
        query = select(Wallet)
        for key, value in filters.items():
            if hasattr(Wallet, key):
                query = query.where(getattr(Wallet, key) == value)
        query = query.limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

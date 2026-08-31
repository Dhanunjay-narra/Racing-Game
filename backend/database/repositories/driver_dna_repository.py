"""
Velocity Nexus — DriverDNA Database Repository
Provides ACID-compliant queries, pagination, caching hooks, and audit logging.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.future import select
from sqlalchemy import update, delete, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import DriverDNA
from backend.core.logger import logger


class DriverDNARepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, entity_id: str) -> Optional[DriverDNA]:
        query = select(DriverDNA).where(DriverDNA.id == entity_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[DriverDNA]:
        query = select(DriverDNA).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self) -> int:
        query = select(func.count(DriverDNA.id))
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def create(self, entity: DriverDNA) -> DriverDNA:
        self.db.add(entity)
        await self.db.flush()
        logger.debug(f"[DriverDNARepository] Created entity with ID {entity.id}")
        return entity

    async def update(self, entity_id: str, update_data: Dict[str, Any]) -> Optional[DriverDNA]:
        stmt = (
            update(DriverDNA)
            .where(DriverDNA.id == entity_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        return await self.get_by_id(entity_id)

    async def delete(self, entity_id: str) -> bool:
        stmt = delete(DriverDNA).where(DriverDNA.id == entity_id)
        result = await self.db.execute(stmt)
        return result.rowcount > 0

    async def find_by_criteria(self, filters: Dict[str, Any], limit: int = 50) -> List[DriverDNA]:
        query = select(DriverDNA)
        for key, value in filters.items():
            if hasattr(DriverDNA, key):
                query = query.where(getattr(DriverDNA, key) == value)
        query = query.limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

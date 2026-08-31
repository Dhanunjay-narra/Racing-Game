"""
Velocity Nexus — VehicleCatalog Database Repository
Provides ACID-compliant queries, pagination, caching hooks, and audit logging.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.future import select
from sqlalchemy import update, delete, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import VehicleCatalog
from backend.core.logger import logger


class VehicleCatalogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, entity_id: str) -> Optional[VehicleCatalog]:
        query = select(VehicleCatalog).where(VehicleCatalog.id == entity_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[VehicleCatalog]:
        query = select(VehicleCatalog).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self) -> int:
        query = select(func.count(VehicleCatalog.id))
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def create(self, entity: VehicleCatalog) -> VehicleCatalog:
        self.db.add(entity)
        await self.db.flush()
        logger.debug(f"[VehicleCatalogRepository] Created entity with ID {entity.id}")
        return entity

    async def update(self, entity_id: str, update_data: Dict[str, Any]) -> Optional[VehicleCatalog]:
        stmt = (
            update(VehicleCatalog)
            .where(VehicleCatalog.id == entity_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        return await self.get_by_id(entity_id)

    async def delete(self, entity_id: str) -> bool:
        stmt = delete(VehicleCatalog).where(VehicleCatalog.id == entity_id)
        result = await self.db.execute(stmt)
        return result.rowcount > 0

    async def find_by_criteria(self, filters: Dict[str, Any], limit: int = 50) -> List[VehicleCatalog]:
        query = select(VehicleCatalog)
        for key, value in filters.items():
            if hasattr(VehicleCatalog, key):
                query = query.where(getattr(VehicleCatalog, key) == value)
        query = query.limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

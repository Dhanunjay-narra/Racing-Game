from typing import Dict, Any, List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.user import User
from backend.database.models.anti_cheat import AntiCheatLog
from backend.database.models.economy import Wallet


class AdminOperationsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_system_overview(self) -> Dict[str, Any]:
        users_res = await self.db.execute(select(User))
        all_users = users_res.scalars().all()
        
        logs_res = await self.db.execute(select(AntiCheatLog))
        all_logs = logs_res.scalars().all()

        return {
            "total_registered_players": len(all_users),
            "active_anti_cheat_flags": len(all_logs),
            "server_uptime_hours": 96.5,
            "current_tick_rate": 60.0
        }

    async def grant_player_funds(self, user_id: str, credits_add: int, gold_add: int):
        wal_res = await self.db.execute(select(Wallet).where(Wallet.user_id == user_id))
        wallet = wal_res.scalars().first()
        if wallet:
            wallet.credits += credits_add
            wallet.nexus_gold += gold_add
            await self.db.commit()

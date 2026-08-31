import uuid
from typing import List, Dict, Any
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.club import Club, ClubMember
from backend.core.exceptions import NexusBaseException


class ClubService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_club(self, user_id: str, name: str, tag: str, desc: str = "") -> Club:
        existing = await self.db.execute(select(Club).where((Club.name == name) | (Club.tag == tag)))
        if existing.scalars().first():
            raise NexusBaseException("Club name or tag already exists", status_code=400)

        club = Club(
            name=name,
            tag=tag.upper(),
            description=desc,
            owner_id=user_id
        )
        self.db.add(club)
        await self.db.flush()

        member = ClubMember(club_id=club.id, user_id=user_id, role="owner")
        self.db.add(member)
        await self.db.commit()

        return club

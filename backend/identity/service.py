from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.user import User, UserSession
from backend.database.models.profile import PlayerProfile
from backend.database.models.economy import Wallet, TransactionLedger
from backend.database.models.driver_dna import DriverDNA
from backend.database.models.vehicle import PlayerVehicle
from backend.identity.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse
from backend.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from backend.core.exceptions import AuthenticationException, NexusBaseException
from backend.core.config import settings
from backend.core.logger import logger


class IdentityService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, req: UserRegisterRequest) -> TokenResponse:
        query = select(User).where((User.username == req.username) | (User.email == req.email))
        result = await self.db.execute(query)
        if result.scalars().first():
            raise NexusBaseException("Username or email already registered", code="USER_EXISTS", status_code=400)

        user = User(
            username=req.username,
            email=req.email,
            hashed_password=hash_password(req.password),
            is_active=True,
            is_verified=True,
            role="driver"
        )
        self.db.add(user)
        await self.db.flush()

        profile = PlayerProfile(
            user_id=user.id,
            display_name=req.display_name or req.username,
            country_code=req.country_code or "GLOBAL",
            level=1,
            xp=0,
            driver_rating=settings.DEFAULT_MMR
        )
        self.db.add(profile)

        wallet = Wallet(
            user_id=user.id,
            credits=settings.STARTING_CREDITS,
            nexus_gold=settings.STARTING_NEXUS_GOLD,
            race_tickets=settings.STARTING_RACE_TICKETS,
            tuning_alloys=150,
            season_tokens=50
        )
        self.db.add(wallet)
        await self.db.flush()

        txn = TransactionLedger(
            wallet_id=wallet.id,
            currency_type="credits",
            amount=settings.STARTING_CREDITS,
            balance_after=settings.STARTING_CREDITS,
            transaction_type="starter_grant",
            description="Welcome to Velocity Nexus starter grant"
        )
        self.db.add(txn)

        driver_dna = DriverDNA(
            user_id=user.id,
            aggression=0.50,
            cornering=0.50,
            overtaking=0.50,
            drifting=0.50,
            consistency=0.50,
            wet_racing=0.50,
            risk_management=0.50,
            driving_archetype="Balanced Prodigy"
        )
        self.db.add(driver_dna)

        starter_car = PlayerVehicle(
            user_id=user.id,
            catalog_vehicle_id="apex_rs1",
            paint_color="#00D2FF",
            paint_finish="Metallic",
            is_favorite=True
        )
        self.db.add(starter_car)

        access_token = create_access_token({"sub": user.id, "username": user.username, "role": user.role})
        refresh_token = create_refresh_token({"sub": user.id})

        user_session = UserSession(
            user_id=user.id,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        self.db.add(user_session)
        await self.db.commit()

        logger.info(f"[Identity] New user registered successfully: '{user.username}' (ID: {user.id})")

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            username=user.username,
            display_name=profile.display_name,
            role=user.role,
            level=profile.level,
            credits=wallet.credits,
            nexus_gold=wallet.nexus_gold
        )

    async def authenticate_user(self, req: UserLoginRequest) -> TokenResponse:
        query = select(User).where(
            (User.username == req.username_or_email) | (User.email == req.username_or_email)
        )
        result = await self.db.execute(query)
        user = result.scalars().first()

        if not user or not verify_password(req.password, user.hashed_password):
            raise AuthenticationException("Invalid username/email or password")

        if not user.is_active:
            raise AuthenticationException("Account has been suspended")

        user.last_login = datetime.utcnow()
        await self.db.commit()

        prof_res = await self.db.execute(select(PlayerProfile).where(PlayerProfile.user_id == user.id))
        profile = prof_res.scalars().first()

        wal_res = await self.db.execute(select(Wallet).where(Wallet.user_id == user.id))
        wallet = wal_res.scalars().first()

        access_token = create_access_token({"sub": user.id, "username": user.username, "role": user.role})
        refresh_token = create_refresh_token({"sub": user.id})

        user_session = UserSession(
            user_id=user.id,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        self.db.add(user_session)
        await self.db.commit()

        logger.info(f"[Identity] User logged in: '{user.username}'")

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            username=user.username,
            display_name=profile.display_name if profile else user.username,
            role=user.role,
            level=profile.level if profile else 1,
            credits=wallet.credits if wallet else 0,
            nexus_gold=wallet.nexus_gold if wallet else 0
        )

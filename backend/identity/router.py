from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.session import get_db
from backend.identity.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse
from backend.identity.service import IdentityService
from backend.core.exceptions import NexusBaseException

router = APIRouter(prefix="/auth", tags=["Authentication & Identity"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    service = IdentityService(db)
    try:
        return await service.register_user(req)
    except NexusBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/login", response_model=TokenResponse)
async def login(req: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    service = IdentityService(db)
    try:
        return await service.authenticate_user(req)
    except NexusBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

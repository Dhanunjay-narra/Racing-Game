from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from backend.database.session import get_db
from backend.economy.service import EconomyService
from backend.core.exceptions import NexusBaseException

router = APIRouter(prefix="/economy", tags=["Virtual Economy & Wallets"])


class TransactionRequest(BaseModel):
    user_id: str
    currency_type: str
    amount: int
    transaction_type: str
    description: str


@router.get("/wallet/{user_id}")
async def get_user_wallet(user_id: str, db: AsyncSession = Depends(get_db)):
    service = EconomyService(db)
    try:
        wallet = await service.get_wallet(user_id)
        return {
            "user_id": user_id,
            "credits": wallet.credits,
            "nexus_gold": wallet.nexus_gold,
            "race_tickets": wallet.race_tickets,
            "tuning_alloys": wallet.tuning_alloys,
            "season_tokens": wallet.season_tokens
        }
    except NexusBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/transact")
async def execute_transaction(req: TransactionRequest, db: AsyncSession = Depends(get_db)):
    service = EconomyService(db)
    try:
        txn = await service.process_transaction(
            user_id=req.user_id,
            currency_type=req.currency_type,
            amount=req.amount,
            transaction_type=req.transaction_type,
            description=req.description
        )
        return {
            "transaction_id": txn.id,
            "balance_after": txn.balance_after,
            "amount": txn.amount,
            "currency": txn.currency_type
        }
    except NexusBaseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

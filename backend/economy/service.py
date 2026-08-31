from typing import Dict, Any, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models.economy import Wallet, TransactionLedger
from backend.core.exceptions import InsufficientFundsException, EntityNotFoundException
from backend.core.logger import logger


class EconomyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_wallet(self, user_id: str) -> Wallet:
        res = await self.db.execute(select(Wallet).where(Wallet.user_id == user_id))
        wallet = res.scalars().first()
        if not wallet:
            raise EntityNotFoundException("Wallet", user_id)
        return wallet

    async def process_transaction(
        self,
        user_id: str,
        currency_type: str,
        amount: int,
        transaction_type: str,
        description: str,
        reference_id: Optional[str] = None
    ) -> TransactionLedger:
        wallet = await self.get_wallet(user_id)
        
        current_balance = getattr(wallet, currency_type, None)
        if current_balance is None:
            raise ValueError(f"Unknown currency type: {currency_type}")

        new_balance = current_balance + amount
        if new_balance < 0:
            raise InsufficientFundsException(currency_type, abs(amount), current_balance)

        setattr(wallet, currency_type, new_balance)

        ledger_entry = TransactionLedger(
            wallet_id=wallet.id,
            currency_type=currency_type,
            amount=amount,
            balance_after=new_balance,
            transaction_type=transaction_type,
            reference_id=reference_id,
            description=description
        )
        self.db.add(ledger_entry)
        await self.db.commit()

        logger.info(f"[Economy] User {user_id} {currency_type} {amount:+d} -> Balance: {new_balance} ({transaction_type})")
        return ledger_entry

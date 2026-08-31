import uuid
import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.matchmaking.service import matchmaking_queue, MatchmakingTicket

router = APIRouter(prefix="/matchmaking", tags=["Matchmaking Service"])


class JoinQueueRequest(BaseModel):
    user_id: str
    username: str
    mmr: int = 1200
    region: str = "NA"
    vehicle_id: str = "apex_rs1"
    race_mode: str = "Circuit"


@router.post("/join")
async def join_queue(req: JoinQueueRequest):
    ticket = MatchmakingTicket(
        ticket_id=str(uuid.uuid4()),
        user_id=req.user_id,
        username=req.username,
        mmr=req.mmr,
        region=req.region,
        vehicle_id=req.vehicle_id,
        race_mode=req.race_mode,
        created_at=time.time()
    )
    await matchmaking_queue.enqueue(ticket)
    return {
        "status": "QUEUED",
        "ticket_id": ticket.ticket_id,
        "estimated_wait_seconds": 5
    }


@router.delete("/leave/{user_id}")
async def leave_queue(user_id: str):
    await matchmaking_queue.dequeue(user_id)
    return {"status": "DEQUEUED"}

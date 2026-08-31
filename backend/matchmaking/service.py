import time
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class MatchmakingTicket:
    ticket_id: str
    user_id: str
    username: str
    mmr: int
    region: str
    vehicle_id: str
    race_mode: str
    created_at: float


class MatchmakingQueue:
    def __init__(self):
        self.tickets: List[MatchmakingTicket] = []
        self._lock = asyncio.Lock()

    async def enqueue(self, ticket: MatchmakingTicket):
        async with self._lock:
            self.tickets.append(ticket)

    async def dequeue(self, user_id: str):
        async with self._lock:
            self.tickets = [t for t in self.tickets if t.user_id != user_id]

    async def find_matches(self, max_players_per_match: int = 4) -> List[List[MatchmakingTicket]]:
        async with self._lock:
            matches: List[List[MatchmakingTicket]] = []
            if len(self.tickets) < 2:
                return matches

            now = time.time()
            unmatched = list(self.tickets)
            
            while len(unmatched) >= 2:
                primary = unmatched.pop(0)
                queue_duration = now - primary.created_at
                
                # Expand allowed MMR tolerance over wait time
                allowed_delta = 100 + int(queue_duration * 25)
                
                group = [primary]
                for other in list(unmatched):
                    if abs(other.mmr - primary.mmr) <= allowed_delta and other.race_mode == primary.race_mode:
                        group.append(other)
                        unmatched.remove(other)
                        if len(group) >= max_players_per_match:
                            break
                            
                if len(group) >= 2:
                    matches.append(group)
                    for member in group:
                        if member in self.tickets:
                            self.tickets.remove(member)
                else:
                    break

            return matches


matchmaking_queue = MatchmakingQueue()

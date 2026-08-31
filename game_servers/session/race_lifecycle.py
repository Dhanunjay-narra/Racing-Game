import time
from enum import Enum
from typing import Dict, List, Any


class RaceState(Enum):
    LOBBY = "LOBBY"
    COUNTDOWN = "COUNTDOWN"
    RACING = "RACING"
    FINISHED = "FINISHED"
    TERMINATED = "TERMINATED"


class RaceRoomSession:
    def __init__(self, room_id: str, track_id: str, total_laps: int = 3, max_players: int = 8):
        self.room_id = room_id
        self.track_id = track_id
        self.total_laps = total_laps
        self.max_players = max_players
        self.state = RaceState.LOBBY
        
        self.players: Dict[str, Dict[str, Any]] = {}
        self.spectators: List[str] = []
        self.start_time: float = 0.0
        self.countdown_remaining: float = 3.0
        self.finished_podium: List[Dict[str, Any]] = []

    def add_player(self, player_id: str, username: str, vehicle_id: str):
        if len(self.players) < self.max_players:
            self.players[player_id] = {
                "id": player_id,
                "username": username,
                "vehicle_id": vehicle_id,
                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                "rotation_y": 0.0,
                "speed_kmh": 0.0,
                "current_lap": 1,
                "current_checkpoint": 0,
                "lap_times_ms": [],
                "finished": False,
                "finish_time_ms": 0
            }

    def start_countdown(self):
        if self.state == RaceState.LOBBY:
            self.state = RaceState.COUNTDOWN
            self.countdown_remaining = 3.0

    def update_tick(self, dt: float):
        if self.state == RaceState.COUNTDOWN:
            self.countdown_remaining -= dt
            if self.countdown_remaining <= 0.0:
                self.state = RaceState.RACING
                self.start_time = time.time()

        elif self.state == RaceState.RACING:
            # Check if all players finished
            all_done = all(p["finished"] for p in self.players.values()) if self.players else False
            if all_done and len(self.players) > 0:
                self.state = RaceState.FINISHED

    def record_player_checkpoint(self, player_id: str, checkpoint_idx: int, is_lap_complete: bool, lap_time_ms: int):
        if player_id in self.players:
            p = self.players[player_id]
            p["current_checkpoint"] = checkpoint_idx
            
            if is_lap_complete:
                p["lap_times_ms"].append(lap_time_ms)
                if p["current_lap"] >= self.total_laps:
                    p["finished"] = True
                    total_time = sum(p["lap_times_ms"])
                    p["finish_time_ms"] = total_time
                    self.finished_podium.append({
                        "player_id": player_id,
                        "username": p["username"],
                        "position": len(self.finished_podium) + 1,
                        "total_time_ms": total_time,
                        "best_lap_ms": min(p["lap_times_ms"])
                    })
                else:
                    p["current_lap"] += 1

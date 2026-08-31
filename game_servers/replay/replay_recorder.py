import time
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ReplayFrame:
    frame_idx: int
    timestamp_ms: int
    player_states: Dict[str, Dict[str, Any]]


class ReplayRecorder:
    def __init__(self, race_id: str, track_id: str):
        self.race_id = race_id
        self.track_id = track_id
        self.frames: List[ReplayFrame] = []
        self.start_time_ms: int = int(time.time() * 1000)

    def record_tick(self, frame_idx: int, player_states: Dict[str, Dict[str, Any]]):
        now = int(time.time() * 1000) - self.start_time_ms
        frame = ReplayFrame(
            frame_idx=frame_idx,
            timestamp_ms=now,
            player_states=player_states
        )
        self.frames.append(frame)

    def export_json(self) -> str:
        return json.dumps({
            "race_id": self.race_id,
            "track_id": self.track_id,
            "total_frames": len(self.frames),
            "frames": [
                {
                    "idx": f.frame_idx,
                    "t": f.timestamp_ms,
                    "players": f.player_states
                }
                for f in self.frames
            ]
        })

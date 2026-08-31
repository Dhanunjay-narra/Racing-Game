import json
import time
from typing import Dict, Any, Tuple


class PacketType:
    HANDSHAKE = "HANDSHAKE"
    HEARTBEAT = "HEARTBEAT"
    INPUT_FRAME = "INPUT_FRAME"
    WORLD_STATE = "WORLD_STATE"
    RACE_EVENT = "RACE_EVENT"
    CHECKPOINT_PASSED = "CHECKPOINT_PASSED"
    RACE_FINISHED = "RACE_FINISHED"


class PacketSerializer:
    @staticmethod
    def encode(packet_type: str, sequence_num: int, payload: Dict[str, Any]) -> str:
        data = {
            "t": packet_type,
            "seq": sequence_num,
            "ts": int(time.time() * 1000),
            "d": payload
        }
        return json.dumps(data)

    @staticmethod
    def decode(raw_str: str) -> Tuple[str, int, Dict[str, Any]]:
        try:
            data = json.loads(raw_str)
            return data.get("t", "UNKNOWN"), data.get("seq", 0), data.get("d", {})
        except Exception:
            return "MALFORMED", 0, {}

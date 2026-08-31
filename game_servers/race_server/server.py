import asyncio
import websockets
import json
from typing import Dict, Set
from backend.core.logger import logger
from game_servers.networking.packet_manager import PacketSerializer, PacketType
from game_servers.session.race_lifecycle import RaceRoomSession, RaceState


class RealTimeRaceServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.rooms: Dict[str, RaceRoomSession] = {}
        self.clients: Dict[websockets.WebSocketServerProtocol, str] = {}
        self.is_running = False

    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        player_id = None
        room_id = "global_room_1"
        
        if room_id not in self.rooms:
            self.rooms[room_id] = RaceRoomSession(room_id=room_id, track_id="neon_cyber_city")
            
        session = self.rooms[room_id]
        
        try:
            async for message in websocket:
                pkt_type, seq, payload = PacketSerializer.decode(message)
                
                if pkt_type == PacketType.HANDSHAKE:
                    player_id = payload.get("user_id", "guest")
                    username = payload.get("username", "Racer")
                    car_id = payload.get("vehicle_id", "apex_rs1")
                    self.clients[websocket] = player_id
                    session.add_player(player_id, username, car_id)
                    
                    ack = PacketSerializer.encode("HANDSHAKE_ACK", seq, {
                        "room_id": room_id,
                        "player_count": len(session.players),
                        "track_id": session.track_id
                    })
                    await websocket.send(ack)

                elif pkt_type == PacketType.INPUT_FRAME and player_id:
                    # Update player state
                    if player_id in session.players:
                        p = session.players[player_id]
                        p["position"] = payload.get("pos", p["position"])
                        p["rotation_y"] = payload.get("rot_y", p["rotation_y"])
                        p["speed_kmh"] = payload.get("speed", p["speed_kmh"])

                elif pkt_type == PacketType.CHECKPOINT_PASSED and player_id:
                    cp_idx = payload.get("checkpoint_idx", 0)
                    lap_done = payload.get("lap_complete", False)
                    lap_time = payload.get("lap_time_ms", 0)
                    session.record_player_checkpoint(player_id, cp_idx, lap_done, lap_time)

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            if websocket in self.clients:
                del self.clients[websocket]

    async def broadcast_tick_loop(self):
        tick_interval = 1.0 / 60.0  # 60 Hz
        seq = 0
        while self.is_running:
            start_time = asyncio.get_event_loop().time()
            seq += 1
            
            for room_id, session in self.rooms.items():
                session.update_tick(tick_interval)
                state_packet = PacketSerializer.encode(PacketType.WORLD_STATE, seq, {
                    "state": session.state.value,
                    "countdown": session.countdown_remaining,
                    "players": session.players,
                    "podium": session.finished_podium
                })
                
                # Broadcast
                for ws, p_id in list(self.clients.items()):
                    try:
                        await ws.send(state_packet)
                    except Exception:
                        pass
                        
            elapsed = asyncio.get_event_loop().time() - start_time
            sleep_dur = max(0.001, tick_interval - elapsed)
            await asyncio.sleep(sleep_dur)

    async def start(self):
        self.is_running = True
        logger.info(f"[RaceServer] 60Hz Authoritative Race Server running on ws://{self.host}:{self.port}")
        server = await websockets.serve(self.handle_client, self.host, self.port)
        asyncio.create_task(self.broadcast_tick_loop())
        await server.wait_closed()


if __name__ == "__main__":
    server = RealTimeRaceServer()
    asyncio.run(server.start())

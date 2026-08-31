from typing import Any

class NexusBaseException(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class EntityNotFoundException(NexusBaseException):
    def __init__(self, entity_name: str, entity_id: Any = None):
        msg = f"{entity_name} with identifier '{entity_id}' not found." if entity_id else f"{entity_name} not found."
        super().__init__(msg, code="NOT_FOUND", status_code=404)


class AuthenticationException(NexusBaseException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, code="UNAUTHORIZED", status_code=401)


class AuthorizationException(NexusBaseException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, code="FORBIDDEN", status_code=403)


class InsufficientFundsException(NexusBaseException):
    def __init__(self, currency: str, required: float, available: float):
        super().__init__(
            f"Insufficient {currency}: required {required}, available {available}",
            code="INSUFFICIENT_FUNDS",
            status_code=400
        )


class MatchmakingException(NexusBaseException):
    def __init__(self, message: str):
        super().__init__(message, code="MATCHMAKING_ERROR", status_code=400)


class PhysicsAnomalyException(NexusBaseException):
    def __init__(self, player_id: str, anomaly_type: str, details: str):
        super().__init__(
            f"Physics anomaly detected for player {player_id}: [{anomaly_type}] {details}",
            code="PHYSICS_ANOMALY",
            status_code=400
        )

from uuid import UUID

from pydantic import BaseModel


class Movement(BaseModel):
    matchId: UUID
    playerId: str
    position: dict[str, int]

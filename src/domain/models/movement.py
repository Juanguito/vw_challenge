from uuid import UUID

from pydantic import BaseModel


class Movement(BaseModel):
    matchId: UUID
    playerId: str
    position: dict[str, int]

    def __str__(self):
        return (
            f"Match: {self.matchId}\n"
            + f"Player: {self.playerId}\n"
            + f"Position: {self.position}"
        )

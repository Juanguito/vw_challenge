import json
from uuid import UUID

from pydantic import BaseModel

from src.domain.models.status import Status


class Match(BaseModel):
    id: UUID
    board: list[list[str | None]]
    turn: str
    status: Status

    def __str__(self):
        return (
            f"Match: {self.id}\n"
            + f"Turn: {self.turn}\n"
            + f"Status: {self.status}\n"
            + f"Board: {json.dumps(self.board)}"
        )

import json
from uuid import UUID

from src.domain.models.status import Status


class Match:
    id: UUID
    board: list[list[str | None]]
    turn: str
    status: Status

    def __init__(
        self, id: UUID, board: list[list[str | None]], turn: str, status: Status
    ):
        self.id = id
        self.board = board
        self.turn = turn
        self.status = status

    def __str__(self):
        return (
            f"Match: {self.id}\n"
            + f"Turn: {self.turn}\n"
            + f"Status: {self.status}\n"
            + f"Board: {json.dumps(self.board)}"
        )

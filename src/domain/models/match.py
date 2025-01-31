from uuid import UUID

from pydantic import BaseModel

from src.domain.models.status import Status


class Match(BaseModel):
    id: UUID
    board: list[list[str | None]]
    turn: str
    status: Status

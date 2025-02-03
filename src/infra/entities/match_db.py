import json
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.orm import DeclarativeBase

from src.domain.models.match import Match
from src.domain.models.status import Status


class Base(DeclarativeBase):
    pass


class MatchDB(Base):
    __tablename__ = "matches"

    id = Column(UUID_PG(as_uuid=True), primary_key=True, default=uuid4, index=True)
    status = Column(String, nullable=False)
    turn = Column(String, nullable=False)
    board = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    @staticmethod
    def board_to_string(board: list[list[str | None]]) -> str:
        return json.dumps(board)

    @staticmethod
    def string_to_board(board: str) -> list[list[str | None]]:
        return json.loads(board)

    @staticmethod
    def from_match(match: Match) -> "MatchDB":
        return MatchDB(
            id=match.id,
            status=match.status.value,
            turn=match.turn,
            board=MatchDB.board_to_string(match.board),
        )

    def to_match(self) -> Match:
        return Match(
            id=UUID(str(self.id)),
            status=Status(self.status),
            turn=str(self.turn),
            board=MatchDB.string_to_board(str(self.board)),
        )

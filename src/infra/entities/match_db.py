import json
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.domain.models.match import Match
from src.domain.models.status import Status


class Base(DeclarativeBase):
    pass


class MatchDB(Base):
    __tablename__ = "matches"

    # I found that mypy type errors would be fixed declaring fields this way
    # From https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances
    # and https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table
    id: Mapped[str] = mapped_column(
        UUID_PG(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    status: Mapped[str] = mapped_column(nullable=False)
    turn: Mapped[str] = mapped_column(nullable=False)
    board: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=func.now(), onupdate=func.now()
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

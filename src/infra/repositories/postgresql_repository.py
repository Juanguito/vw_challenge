import json
import os
from uuid import UUID, uuid4

from dotenv import load_dotenv
from sqlalchemy import Column, String, create_engine
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.domain.models.match import Match
from src.domain.models.status import Status
from src.domain.repositories.match_repository import MatchRepository

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class Base(DeclarativeBase):
    pass


class MatchDB(Base):
    __tablename__ = "matches"

    id = Column(UUID_PG(as_uuid=True), primary_key=True, default=uuid4, index=True)
    status = Column(String, nullable=False)
    turn = Column(String, nullable=False)
    board = Column(String, nullable=False)

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
            id=self.id,
            status=Status(self.status),
            turn=str(self.turn),
            board=MatchDB.string_to_board(str(self.board)),
        )


class PostgreSQLRepository(MatchRepository):

    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(bind=self.engine)

    def save_match(self, match: Match) -> Match:
        db = self.SessionLocal()
        try:
            match_db = MatchDB.from_match(match)

            db.add(match_db)
            db.commit()
            db.refresh(match_db)

            return match_db.to_match()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error saving match: {e}")
        finally:
            db.close()

    def update_match(self, match: Match) -> Match:
        db = self.SessionLocal()
        try:
            if match_db := db.query(MatchDB).filter(MatchDB.id == match.id).first():
                match_db.status = match.status.value
                match_db.turn = match.turn
                match_db.board = MatchDB.board_to_string(match.board)

                db.commit()
                db.refresh(match_db)

                return match_db.to_match()
            else:
                raise Exception("Match not found")

        except Exception as e:
            db.rollback()
            raise Exception(f"Error updating match: {e}")
        finally:
            db.close()

    def get_match(self, match_id: UUID) -> Match | None:
        db = self.SessionLocal()
        try:
            if match_db := db.query(MatchDB).filter(MatchDB.id == match_id).first():
                return match_db.to_match()
            else:
                return None
        except Exception as e:
            raise Exception(f"Error getting match: {e}")
        finally:
            db.close()

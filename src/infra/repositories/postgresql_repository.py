import os
from uuid import UUID

from dotenv import load_dotenv
from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import sessionmaker

from src.domain.exception.errors import (
    DatabaseEnvVarNotSetException,
    DatabaseGetMatchException,
    DatabaseMatchNotFoundException,
    DatabaseSaveMatchException,
    DatabaseUpdateMatchException,
)
from src.domain.logging.logger_interface import LoggerInterface
from src.domain.models.match import Match
from src.domain.repositories.match_database_repository import MatchDatabaseRepository
from src.infra.entities.match_db import Base, MatchDB

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class PostgreSQLRepository(MatchDatabaseRepository):

    def __init__(self, logger: LoggerInterface):
        self.logger = logger

        if DATABASE_URL is None:
            raise DatabaseEnvVarNotSetException("DATABASE_URL env variable is not set")

        self.engine = create_engine(DATABASE_URL)

        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(bind=self.engine)

    def save_match(self, match: Match) -> Match:
        self.logger.info(f"Saving match:\n{match}")

        try:
            with self.SessionLocal() as session:
                match_db = MatchDB.from_match(match)

                stmt = insert(MatchDB).values(
                    id=match_db.id,
                    status=match_db.status,
                    turn=match_db.turn,
                    board=match_db.board,
                )
                session.execute(stmt)
                session.commit()

                self.logger.info(f"Match: {match_db.id} SAVED!")

                return match_db.to_match()
        except Exception as e:
            self.logger.error(f"Error saving match:{match}\nError: {e}")
            raise DatabaseSaveMatchException(f"Error saving match: {e}")

    def update_match(self, match: Match) -> Match:
        self.logger.info(f"Updating match:\n{match}")

        try:
            with self.SessionLocal() as session:
                statement = select(MatchDB).filter(MatchDB.id == match.id)
                if match_instance := session.execute(statement).scalar_one_or_none():
                    match_instance.status = match.status.value
                    match_instance.turn = match.turn
                    match_instance.board = MatchDB.board_to_string(match.board)

                    session.commit()

                    self.logger.info(f"Match: {match} UPDATED!")

                    return match_instance.to_match()
                else:
                    raise DatabaseMatchNotFoundException("Match not found")
        except DatabaseMatchNotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error updating match:{match}\nError: {e}")
            raise DatabaseUpdateMatchException(f"Error updating match: {e}")

    def get_match(self, match_id: UUID) -> Match | None:
        self.logger.info(f"Retrieving match:\n{match_id}")

        try:
            with self.SessionLocal() as session:
                statement = select(MatchDB).filter(MatchDB.id == match_id)
                if match_instance := session.execute(statement).scalar_one_or_none():
                    match = match_instance.to_match()
                    self.logger.info(f"Match: {match} RETRIEVED!")

                    return match

                return None
        except Exception as e:
            self.logger.error(f"Error getting match!\nMatch:{match_id}\nError: {e}")
            raise DatabaseGetMatchException(f"Error getting match: {e}")

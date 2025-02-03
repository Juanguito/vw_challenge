import os
from uuid import UUID

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.errors import (
    DatabaseEnvVarNotSetException,
    DatabaseGetMatchException,
    DatabaseMatchNotFoundException,
    DatabaseSaveMatchException,
    DatabaseUpdateMatchException,
)
from src.domain.models.match import Match
from src.domain.repositories.match_database_repository import MatchDatabaseRepository
from src.domain.services.logger_interface import LoggerInterface
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
        db = self.SessionLocal()
        try:
            self.logger.info(f"Saving match:\n{match}")
            match_db = MatchDB.from_match(match)

            db.add(match_db)
            db.commit()
            db.refresh(match_db)
            self.logger.info("Match SAVED")

            return match_db.to_match()

        except Exception as e:
            db.rollback()
            self.logger.error(f"Error saving match:{match}\nError: {e}")
            raise DatabaseSaveMatchException(f"Error saving match: {e}")
        finally:
            db.close()

    def update_match(self, match: Match) -> Match:
        db = self.SessionLocal()
        try:
            self.logger.info(f"Updating match:\n{match}")
            if match_db := db.query(MatchDB).filter(MatchDB.id == match.id).first():
                match_db.status = match.status.value
                match_db.turn = match.turn
                match_db.board = MatchDB.board_to_string(match.board)

                db.commit()
                db.refresh(match_db)
                self.logger.info("Match UPDATED!")

                return match_db.to_match()
            else:
                raise DatabaseMatchNotFoundException("Match not found")

        except Exception as e:
            db.rollback()
            self.logger.error(f"Error updating match:{match}\nError: {e}")
            raise DatabaseUpdateMatchException(f"Error updating match: {e}")
        finally:
            db.close()

    def get_match(self, match_id: UUID) -> Match | None:
        db = self.SessionLocal()
        try:
            self.logger.info(f"Retrieving match:\n{match_id}")
            if match_db := db.query(MatchDB).filter(MatchDB.id == match_id).first():
                match = match_db.to_match()
                self.logger.info(f"Match: {match} RETRIEVED!")

                return match
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error getting match!\nMatch:{match_id}\nError: {e}")
            raise DatabaseGetMatchException(f"Error getting match: {e}")
        finally:
            db.close()

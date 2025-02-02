import logging
import sys
from uuid import UUID

from fastapi import APIRouter

from src.domain.models.movement import Movement
from src.domain.services.match_service import MatchService
from src.infra.repositories.logging_service import LoggingService
from src.infra.repositories.postgresql_repository import PostgreSQLRepository

router = APIRouter()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)

logger = LoggingService()
match_repository = PostgreSQLRepository(logger)
match_service = MatchService(match_repository, logger)


@router.get("/create")
def create_match() -> dict:
    logger.info("Create match request received")
    match = match_service.create_match()

    return {
        "matchId": match.id,
        "turn": match.turn,
    }


@router.post("/move")
def move(movement: Movement) -> dict:
    logger.info(f"New movement request received: {movement}")
    message = match_service.move(movement)

    return {"message": message}


@router.get("/status/{matchId}")
def match_status(matchId: UUID) -> dict:
    logger.info(f"Get match status request received: {matchId}")
    status = match_service.get_match_status(matchId)

    return {"status": status}

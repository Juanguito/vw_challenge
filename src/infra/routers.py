import logging
import sys
from uuid import UUID

from fastapi import APIRouter

from src.application.create_match_usecase import CreateMatchUseCase
from src.application.get_match_status_usecase import GetMatchStatusUseCase
from src.application.make_movement_usecase import MakeMovementUseCase
from src.domain.errors import to_http_exception
from src.domain.models.movement import Movement
from src.infra.logging_service import LoggingService
from src.infra.repositories.postgresql_repository import PostgreSQLRepository

router = APIRouter()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)

logger = LoggingService()


@router.get("/create")
def create_match() -> dict:
    logger.info("Create match request received")

    try:
        match = CreateMatchUseCase(
            match_database_repository=PostgreSQLRepository(logger=logger),
            logger=logger,
        ).run()
    except Exception as e:
        raise to_http_exception(e)

    return {
        "matchId": match.id,
        "turn": match.turn,
    }


@router.post("/move")
def move(movement: Movement) -> dict:
    logger.info(f"New movement request received: {movement}")

    try:
        message = MakeMovementUseCase(
            match_database_repository=PostgreSQLRepository(logger=logger),
            logger=logger,
        ).run(movement=movement)
    except Exception as e:
        raise to_http_exception(e)

    return {"message": message}


@router.get("/status/{matchId}")
def match_status(matchId: UUID) -> dict:
    logger.info(f"Get match status request received: {matchId}")

    try:
        status = GetMatchStatusUseCase(
            match_database_repository=PostgreSQLRepository(logger=logger),
            logger=logger,
        ).run(match_id=matchId)
    except Exception as e:
        raise to_http_exception(e)

    return {"status": status}

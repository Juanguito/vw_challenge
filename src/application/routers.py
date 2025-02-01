from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from src.domain.models.movement import Movement
from src.domain.services.match_service import MatchService
from src.infra.repositories.in_memory_repository import InMemoryRepository
from src.infra.repositories.postgresql_repository import PostgreSQLRepository

router = APIRouter()

match_repository = PostgreSQLRepository()
match_service = MatchService(match_repository)


@router.get("/create")
def create_match() -> dict:
    match = match_service.create_match()

    return {
        "matchId": match.id,
        "turn": match.turn,
    }


@router.post("/move")
def move(movement: Movement) -> dict:
    message = match_service.move(movement)

    return {"message": message}


@router.get("/status/{matchId}")
def match_status(matchId: UUID) -> dict:
    status = match_service.get_match_status(matchId)

    return {"status": status}

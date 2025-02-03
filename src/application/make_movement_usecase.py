from src.domain.models.movement import Movement
from src.domain.services.match_service import MatchService
from src.infra.logging_service import LoggingService
from src.infra.repositories.postgresql_repository import PostgreSQLRepository


class MakeMovementUseCase:
    def __init__(self):
        self.logger = LoggingService()
        self.match_repository = PostgreSQLRepository(self.logger)
        self.match_service = MatchService(self.match_repository, self.logger)

    def run(self, movement: Movement) -> str:
        return self.match_service.move(movement)

from src.domain.logging.logger_interface import LoggerInterface
from src.domain.models.movement import Movement
from src.domain.repositories.match_database_repository import MatchDatabaseRepository
from src.domain.services.match_service import MatchService


class MakeMovementUseCase:
    def __init__(
        self,
        match_database_repository: MatchDatabaseRepository,
        logger: LoggerInterface,
    ):
        self.match_service = MatchService(match_database_repository, logger)

    def run(self, movement: Movement) -> str:
        return self.match_service.move(movement)

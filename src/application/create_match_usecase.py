from src.domain.models.match import Match
from src.domain.repositories.match_database_repository import MatchDatabaseRepository
from src.domain.services.logger_interface import LoggerInterface
from src.domain.services.match_service import MatchService


class CreateMatchUseCase:
    def __init__(
        self,
        match_database_repository: MatchDatabaseRepository,
        logger: LoggerInterface,
    ):
        self.match_service = MatchService(match_database_repository, logger)

    def run(self) -> Match:
        return self.match_service.create_match()

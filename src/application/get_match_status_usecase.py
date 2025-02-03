from uuid import UUID

from src.domain.models.status import Status
from src.domain.repositories.match_database_repository import MatchDatabaseRepository
from src.domain.services.logger_interface import LoggerInterface
from src.domain.services.match_service import MatchService


class GetMatchStatusUseCase:
    def __init__(
        self,
        match_database_repository: MatchDatabaseRepository,
        logger: LoggerInterface,
    ):
        self.match_service = MatchService(match_database_repository, logger)

    def run(self, match_id: UUID) -> Status:
        return self.match_service.get_match_status(match_id)

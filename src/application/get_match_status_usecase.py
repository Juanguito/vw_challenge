from uuid import UUID

from src.domain.models.status import Status
from src.domain.services.match_service import MatchService
from src.infra.logging_service import LoggingService
from src.infra.repositories.postgresql_repository import PostgreSQLRepository


class GetMatchStatusUseCase:
    def __init__(self):
        self.logger = LoggingService()
        self.match_repository = PostgreSQLRepository(self.logger)
        self.match_service = MatchService(self.match_repository, self.logger)

    def run(self, match_id: UUID) -> Status:
        return self.match_service.get_match_status(match_id)

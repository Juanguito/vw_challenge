from src.domain.models.match import Match
from src.domain.services.match_service import MatchService
from src.infra.logging_service import LoggingService
from src.infra.repositories.postgresql_repository import PostgreSQLRepository


class CreateMatchUseCase:
    def __init__(self):
        self.logger = LoggingService()
        self.match_repository = PostgreSQLRepository(self.logger)
        self.match_service = MatchService(self.match_repository, self.logger)

    def run(self) -> Match:
        return self.match_service.create_match()

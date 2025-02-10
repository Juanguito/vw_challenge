from uuid import UUID

from src.domain.logging.logger_interface import LoggerInterface
from src.domain.models.match import Match
from src.domain.repositories.match_database_repository import MatchDatabaseRepository


class InMemoryRepository(MatchDatabaseRepository):
    cache: dict[UUID, Match] = {}

    def __init__(self, logger: LoggerInterface):
        self.logger = logger

    def get_match(self, match_id: UUID) -> Match | None:
        return self.cache.get(match_id)

    def save_match(self, match: Match) -> Match:
        self.cache[match.id] = match
        return match

    def update_match(self, match: Match) -> Match:
        self.cache[match.id] = match
        return match

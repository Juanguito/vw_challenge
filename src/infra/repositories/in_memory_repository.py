from uuid import UUID

from src.domain.models.match import Match
from src.domain.repositories.match_repository import MatchRepository


class InMemoryRepository(MatchRepository):
    cache: dict[UUID, Match] = {}

    def get_match(self, match_id: UUID) -> Match | None:
        return self.cache.get(match_id)

    def save_match(self, match: Match) -> Match:
        self.cache[match.id] = match
        return match

    def update_match(self, match: Match) -> Match:
        self.cache[match.id] = match
        return match

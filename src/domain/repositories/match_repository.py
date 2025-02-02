from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models.match import Match


class MatchRepository(ABC):
    @abstractmethod
    def get_match(self, match_id: UUID) -> Match | None:
        pass

    @abstractmethod
    def save_match(self, match: Match) -> Match:
        pass

    @abstractmethod
    def update_match(self, match: Match) -> Match:
        pass

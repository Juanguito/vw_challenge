from abc import ABC, abstractmethod

from src.domain.models.match import Match


class MatchRepository(ABC):
    @abstractmethod
    def get_match(self, match_id: str) -> Match:
        pass

    @abstractmethod
    def save_match(self, match: Match) -> Match:
        pass

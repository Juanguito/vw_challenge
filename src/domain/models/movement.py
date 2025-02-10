from uuid import UUID


class Movement:
    matchId: UUID
    playerId: str
    square: dict[str, int]

    def __init__(self, matchId: UUID, playerId: str, square: dict[str, int]):
        self.matchId = matchId
        self.playerId = playerId
        self.square = square

    def __str__(self):
        return (
            f"Match: {self.matchId}\n"
            + f"Player: {self.playerId}\n"
            + f"Square: {self.square}"
        )

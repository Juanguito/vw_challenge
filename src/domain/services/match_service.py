import random
import uuid

from src.domain.models.match import Match
from src.domain.models.movement import Movement
from src.domain.models.status import Status
from src.domain.repositories.match_repository import MatchRepository


class MatchService:
    BOARD_SIZE = 3
    PLAYER_IDS = ["X", "O"]

    def __init__(self, match_repository: MatchRepository):
        self.match_repository = match_repository

    def init_board(self) -> list[list[str | None]]:
        board = []
        for _ in range(self.BOARD_SIZE):
            raw = []
            board.append(raw)
            for _ in range(self.BOARD_SIZE):
                raw.append(None)

        return board

    def validate_movement(self, movement: Movement, match: Match) -> None:
        if match.status != Status.PLAYING:
            raise ValueError("Match has already ended")

        if match.turn != movement.playerId:
            raise ValueError("It's not your turn")

        x = movement.position["x"]
        y = movement.position["y"]
        if x >= self.BOARD_SIZE or y >= self.BOARD_SIZE:
            raise ValueError("Position is out of the board")

        if match.board[x][y] is not None:
            raise ValueError("Position is not available")

    def check_same_raw(self, board: list[list[str | None]]) -> bool:
        for row in board:
            value = row[0]
            for i in range(1, self.BOARD_SIZE):
                if row[i] != value:
                    return False

        return True

    def check_same_col(self, board: list[list[str | None]]) -> bool:
        for i in range(0, self.BOARD_SIZE):
            value = board[0][i]
            for row in board:
                if row[i] != value:
                    return False

        return True

    def check_first_diagonal(self, board: list[list[str | None]]) -> bool:
        value = board[0][0]
        for i in range(1, self.BOARD_SIZE):
            if board[i][i] != value:
                return False

        return True

    def check_last_diagonal(self, board: list[list[str | None]]) -> bool:
        value = board[0][self.BOARD_SIZE - 1]
        for i in range(self.BOARD_SIZE - 1, -1, -1):
            if board[i][i] != value:
                return False

        return True

    def check_draw(self, board: list[list[str | None]]) -> bool:
        if all(
            board[x][y] is not None
            for x in range(self.BOARD_SIZE)
            for y in range(self.BOARD_SIZE)
        ):
            return True

    def check_movement(self, board: list[list[str | None]]) -> Status:
        if self.check_same_raw(board):
            return Status.WINNER

        if self.check_same_col(board):
            return Status.WINNER

        if self.check_first_diagonal(board):
            return Status.WINNER

        if self.check_last_diagonal(board):
            return Status.WINNER

        if self.check_draw(board):
            return Status.DRAW

        return Status.PLAYING

    def create_match(self) -> Match:
        match = Match(
            id=uuid.uuid4(),
            board=self.init_board(),
            turn=random.choice(self.PLAYER_IDS),
            status=Status.PLAYING,
        )
        self.match_repository.save_match(match)

        return match

    def move(self, movement: Movement) -> None:
        if match := self.match_repository.get_match(movement.matchId):
            self.validate_movement(movement, match)

            x = movement.position["x"]
            y = movement.position["y"]
            match.board[x][y] = movement.playerId
            match.turn = "O" if match.turn == "X" else "X"

            match.status = self.check_movement(match.board)

            self.match_repository.save_match(match)

        else:
            raise ValueError("Match not found")

    def get_match_status(self, match_id: str) -> Status:
        if match := self.match_repository.get_match(match_id):
            return match.status
        else:
            raise ValueError("Match not found")

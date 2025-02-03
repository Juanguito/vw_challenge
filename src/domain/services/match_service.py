from uuid import UUID, uuid4

from src.domain.errors import (
    MatchAlreadyEndedException,
    MatchNotFoundException,
    PlayerNotValidException,
    SquareNotAvailableException,
    SquareNotValidException,
    SquareOutOfBoundsException,
    TurnNotValidException,
)
from src.domain.models.match import Match
from src.domain.models.movement import Movement
from src.domain.models.status import Status
from src.domain.repositories.match_database_repository import MatchDatabaseRepository
from src.domain.services.logger_interface import LoggerInterface


class MatchService:
    BOARD_SIZE = 3
    PLAYER_IDS = ["X", "O"]
    MOVEMENT_POSITIONS = ["X", "x", "Y", "y"]

    def __init__(
        self,
        match_database_repository: MatchDatabaseRepository,
        logger: LoggerInterface,
    ):
        self.match_database_repository = match_database_repository
        self.logger = logger

    def _init_board(self) -> list[list[str | None]]:
        board: list[list[str | None]] = []
        for _ in range(self.BOARD_SIZE):
            board.append([None for _ in range(self.BOARD_SIZE)])

        return board

    def _get_x(self, square: dict[str, int]) -> int:
        return square["x"] if square.get("x") is not None else square["X"]

    def _get_y(self, square: dict[str, int]) -> int:
        return square["y"] if square.get("y") is not None else square["Y"]

    def _validate_movement(self, movement: Movement, match: Match) -> None:
        if movement.playerId not in self.PLAYER_IDS:
            player_list = [f"{player}" for player in self.PLAYER_IDS]
            self.logger.info(f"Player is not valid: {movement.playerId}")
            raise PlayerNotValidException(
                f"Player is not valid, must be one of: {player_list}"
            )

        if not ("x" in movement.square or "X" in movement.square) or not (
            "y" in movement.square or "Y" in movement.square
        ):
            squares_list = [f"{squares}" for squares in self.MOVEMENT_POSITIONS]
            self.logger.info(f"Square is not valid: {movement.square}")
            raise SquareNotValidException(
                f"Square is not valid, must be one of: {squares_list}",
            )

        if match.status != Status.PLAYING:
            raise MatchAlreadyEndedException(
                f"Match {movement.matchId} has already ended"
            )

        if match.turn != movement.playerId:
            raise TurnNotValidException(
                f"Player {movement.playerId}, it's not your turn"
            )

        x = self._get_x(movement.square)
        y = self._get_y(movement.square)

        if x >= self.BOARD_SIZE or y >= self.BOARD_SIZE:
            self.logger.info(f"Square [{x}, {y}] is out of the board")
            raise SquareOutOfBoundsException(f"Square [{x}, {y}] is out of the board")

        if match.board[x][y] is not None:
            raise SquareNotAvailableException(f"Square [{x}, {y}] is not available")

    def _check_same_row(self, board: list[list[str | None]]) -> bool:
        for row in board:
            value = row[0]
            if value is not None and all(square == value for square in row):
                return True

        return False

    def _check_same_col(self, board: list[list[str | None]]) -> bool:
        for i in range(0, self.BOARD_SIZE):
            value = board[0][i]
            if value is not None and all(row[i] == value for row in board):
                return True

        return False

    def _check_first_diagonal(self, board: list[list[str | None]]) -> bool:
        value = board[0][0]
        if value is not None and all(
            board[i][i] == value for i in range(self.BOARD_SIZE)
        ):
            return True

        return False

    def _check_last_diagonal(self, board: list[list[str | None]]) -> bool:
        j = self.BOARD_SIZE - 1
        value = board[0][j]
        if value is None:
            return False

        for row in board:
            if row[j] != value:
                return False
            j -= 1

        return True

    def _check_draw(self, board: list[list[str | None]]) -> bool:
        if all(
            board[x][y] is not None
            for x in range(self.BOARD_SIZE)
            for y in range(self.BOARD_SIZE)
        ):
            return True

        return False

    def _check_movement(self, board: list[list[str | None]]) -> Status:
        if (
            self._check_same_row(board)
            or self._check_same_col(board)
            or self._check_first_diagonal(board)
            or self._check_last_diagonal(board)
        ):
            return Status.WINNER

        if self._check_draw(board):
            return Status.DRAW

        return Status.PLAYING

    def create_match(self) -> Match:
        match = Match(
            id=uuid4(),
            board=self._init_board(),
            turn="X",  # Convention that X plays first
            status=Status.PLAYING,
        )
        self.match_database_repository.save_match(match)
        self.logger.info(f"Match created: {match.id}")

        return match

    def move(self, movement: Movement) -> str:
        message = ""
        if match := self.match_database_repository.get_match(movement.matchId):
            self._validate_movement(movement, match)

            x = self._get_x(movement.square)
            y = self._get_y(movement.square)
            match.board[x][y] = movement.playerId

            match.status = self._check_movement(match.board)
            match.turn = "O" if match.turn == "X" else "X"
            match match.status:
                case Status.WINNER:
                    message = f"Player '{movement.playerId}' Wins!!!!"
                case Status.DRAW:
                    message = "Draw!!!"
                case Status.PLAYING:
                    message = f"Movement performed. Next turn: {match.turn}"

            self.match_database_repository.update_match(match)

        else:
            raise MatchNotFoundException(f"Match {movement.matchId} not found")

        self.logger.info("Movement performed")

        return message

    def get_match_status(self, match_id: UUID) -> Status:
        if match := self.match_database_repository.get_match(match_id):
            return match.status
        else:
            self.logger.info(f"Match not found: {match_id}")
            raise MatchNotFoundException(f"Match {match_id} not found")

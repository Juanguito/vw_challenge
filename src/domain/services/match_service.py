import random
from uuid import UUID, uuid4

from fastapi import HTTPException

from src.domain.models.match import Match
from src.domain.models.movement import Movement
from src.domain.models.status import Status
from src.domain.repositories.match_repository import MatchRepository


class MatchService:
    BOARD_SIZE = 3
    PLAYER_IDS = ["X", "O"]
    MOVEMENT_POSITIONS = ["X", "x", "Y", "y"]

    def __init__(self, match_repository: MatchRepository):
        self.match_repository = match_repository

    def init_board(self) -> list[list[str | None]]:
        board: list[list[str | None]] = []
        for _ in range(self.BOARD_SIZE):
            board.append([None for _ in range(self.BOARD_SIZE)])

        return board

    def get_x(self, position: dict[str, int]) -> int:
        return position["x"] if position.get("x") is not None else position["X"]

    def get_y(self, position: dict[str, int]) -> int:
        return position["y"] if position.get("y") is not None else position["Y"]

    def validate_movement(self, movement: Movement, match: Match) -> None:
        if movement.playerId not in self.PLAYER_IDS:
            player_list = [f"{player}" for player in self.PLAYER_IDS]
            raise HTTPException(
                status_code=400,
                detail=f"Player is not valid, must be one of: {player_list}",
            )

        if not ("x" in movement.position or "X" in movement.position) or not (
            "y" in movement.position or "Y" in movement.position
        ):
            positions_list = [f"{positions}" for positions in self.MOVEMENT_POSITIONS]
            raise HTTPException(
                status_code=400,
                detail=f"Position is not valid, must be one of: {positions_list}",
            )

        if match.status != Status.PLAYING:
            raise HTTPException(status_code=400, detail="Match has already ended")

        if match.turn != movement.playerId:
            raise HTTPException(status_code=400, detail="It's not your turn")

        x = self.get_x(movement.position)
        y = self.get_y(movement.position)

        if x >= self.BOARD_SIZE or y >= self.BOARD_SIZE:
            raise HTTPException(status_code=400, detail="Position is out of the board")

        if match.board[x][y] is not None:
            raise HTTPException(status_code=400, detail="Position is not available")

    def check_same_row(self, board: list[list[str | None]]) -> bool:
        for row in board:
            value = row[0]
            if value is not None and all(position == value for position in row):
                return True

        return False

    def check_same_col(self, board: list[list[str | None]]) -> bool:
        for i in range(0, self.BOARD_SIZE):
            value = board[0][i]
            if value is not None and all(row[i] == value for row in board):
                return True

        return False

    def check_first_diagonal(self, board: list[list[str | None]]) -> bool:
        value = board[0][0]
        if value is not None and all(
            board[i][i] == value for i in range(self.BOARD_SIZE)
        ):
            return True

        return False

    def check_last_diagonal(self, board: list[list[str | None]]) -> bool:
        j = self.BOARD_SIZE - 1
        value = board[0][j]
        if value is None:
            return False

        for row in board:
            if row[j] != value:
                return False
            j -= 1

        return True

    def check_draw(self, board: list[list[str | None]]) -> bool:
        if all(
            board[x][y] is not None
            for x in range(self.BOARD_SIZE)
            for y in range(self.BOARD_SIZE)
        ):
            return True

        return False

    def check_movement(self, board: list[list[str | None]]) -> Status:
        if (
            self.check_same_row(board)
            or self.check_same_col(board)
            or self.check_first_diagonal(board)
            or self.check_last_diagonal(board)
        ):
            return Status.WINNER

        if self.check_draw(board):
            return Status.DRAW

        return Status.PLAYING

    def create_match(self) -> Match:
        match = Match(
            id=uuid4(),
            board=self.init_board(),
            turn=random.choice(self.PLAYER_IDS),
            status=Status.PLAYING,
        )
        self.match_repository.save_match(match)

        return match

    def move(self, movement: Movement) -> str:
        message = ""
        if match := self.match_repository.get_match(movement.matchId):
            self.validate_movement(movement, match)

            x = self.get_x(movement.position)
            y = self.get_y(movement.position)
            match.board[x][y] = movement.playerId

            match.status = self.check_movement(match.board)
            match.turn = "O" if match.turn == "X" else "X"
            match match.status:
                case Status.WINNER:
                    message = f"Player '{movement.playerId}' Wins!!!!"
                case Status.DRAW:
                    message = "Draw!!!"
                case Status.PLAYING:
                    message = f"Movement performed. Next turn: {match.turn}"

            self.match_repository.update_match(match)

        else:
            raise HTTPException(status_code=404, detail="Match not found")

        return message

    def get_match_status(self, match_id: UUID) -> Status:
        if match := self.match_repository.get_match(match_id):
            return match.status
        else:
            raise HTTPException(status_code=404, detail="Match not found")

import uuid

import pytest
from fastapi import HTTPException

from src.domain.models.movement import Movement
from src.domain.models.status import Status
from src.domain.services.match_service import MatchService
from src.infra.repositories.in_memory_repository import InMemoryRepository


@pytest.fixture
def service():
    return MatchService(match_repository=InMemoryRepository())


def test_create_match(service):
    match = service.create_match()

    assert match is not None
    assert match.status == Status.PLAYING


def test_get_match_status(service):
    match = service.create_match()

    match_status = service.get_match_status(match.id)
    assert match_status == Status.PLAYING


def test_match_status_match_not_found(service):
    service.create_match()

    with pytest.raises(HTTPException, match="Match not found"):
        service.get_match_status(uuid.uuid4())


def test_make_valid_move(service):
    match = service.create_match()
    match.turn = "X"
    movement = Movement(matchId=match.id, playerId="X", position={"x": 0, "y": 0})

    message = service.move(movement)

    assert match.board[0][0] == "X"
    assert match.turn == "O"
    assert match.status == Status.PLAYING
    assert message == "Movement performed. Next turn: O"


def test_row_winner(service):
    match = service.create_match()
    match.turn = "X"
    match.board = [
        [None, None, None],
        ["X", "X", None],
        [None, None, None],
    ]
    movement = Movement(matchId=match.id, playerId="X", position={"x": 1, "y": 2})

    message = service.move(movement)

    assert match.status == Status.WINNER
    assert message == "Player 'X' Wins!!!!"


def test_col_winner(service):
    match = service.create_match()
    match.turn = "X"
    match.board = [
        [None, "X", None],
        [None, "X", None],
        [None, None, None],
    ]
    movement = Movement(matchId=match.id, playerId="X", position={"x": 2, "y": 1})

    message = service.move(movement)

    assert match.status == Status.WINNER
    assert message == "Player 'X' Wins!!!!"


def test_first_diagonal_winner(service):
    match = service.create_match()
    match.turn = "X"
    match.board = [
        ["X", None, None],
        [None, "X", None],
        [None, None, None],
    ]
    movement = Movement(matchId=match.id, playerId="X", position={"x": 2, "y": 2})

    message = service.move(movement)

    assert match.status == Status.WINNER
    assert message == "Player 'X' Wins!!!!"


def test_last_diagonal_winner(service):
    match = service.create_match()
    match.turn = "X"
    match.board = [
        [None, None, "X"],
        [None, "X", None],
        [None, None, None],
    ]
    movement = Movement(matchId=match.id, playerId="X", position={"x": 2, "y": 0})

    message = service.move(movement)

    assert match.status == Status.WINNER
    assert message == "Player 'X' Wins!!!!"


def test_draw(service):
    match = service.create_match()
    match.turn = "X"
    match.board = [
        ["X", "O", None],
        ["X", "O", "O"],
        ["O", "X", "X"],
    ]
    movement = Movement(matchId=match.id, playerId="X", position={"x": 0, "y": 2})

    message = service.move(movement)

    assert match.status == Status.DRAW
    assert message == "Draw!!!"


def test_new_movements_not_allowed(service):
    match = service.create_match()
    match.status = Status.WINNER
    movement1 = Movement(matchId=match.id, playerId="X", position={"x": 0, "y": 0})

    with pytest.raises(HTTPException, match="Match has already ended"):
        service.move(movement1)


def test_invalid_turn(service):
    match = service.create_match()
    match.turn = "O"
    movement = Movement(matchId=match.id, playerId="X", position={"x": 0, "y": 0})

    with pytest.raises(HTTPException, match="It's not your turn"):
        service.move(movement)


def test_position_occupied(service):
    match = service.create_match()
    match.turn = "X"
    match.board[0][0] = "O"
    movement1 = Movement(matchId=match.id, playerId="X", position={"x": 0, "y": 0})

    with pytest.raises(HTTPException, match="Position is not available"):
        service.move(movement1)


def test_x_position_out_of_bounds(service):
    match = service.create_match()
    match.turn = "X"
    movement1 = Movement(matchId=match.id, playerId="X", position={"x": 4, "y": 0})

    with pytest.raises(HTTPException, match="Position is out of the board"):
        service.move(movement1)


def test_y_position_out_of_bounds(service):
    match = service.create_match()
    match.turn = "X"
    movement1 = Movement(matchId=match.id, playerId="X", position={"x": 0, "y": 4})

    with pytest.raises(HTTPException, match="Position is out of the board"):
        service.move(movement1)

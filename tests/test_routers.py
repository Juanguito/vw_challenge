import uuid
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from src.application.create_match_usecase import CreateMatchUseCase
from src.application.get_match_status_usecase import GetMatchStatusUseCase
from src.application.make_movement_usecase import MakeMovementUseCase
from src.infra.repositories.postgresql_repository import PostgreSQLRepository
from src.infra.routers import router

client = TestClient(router)


@patch.object(PostgreSQLRepository, "__init__")
@patch.object(CreateMatchUseCase, "run")
def test_create_match(mock_create_match, mock_postgre):
    id = uuid.uuid4()
    mock_postgre.return_value = None
    mock_create_match.return_value = MagicMock(id=id, turn="X")

    response = client.get("/create")

    assert response.status_code == 200
    assert response.json() == {"matchId": str(id), "turn": "X"}


@patch.object(PostgreSQLRepository, "__init__")
@patch.object(GetMatchStatusUseCase, "run")
def test_get_match_status(mock_get_match_status, mock_postgre):
    mock_postgre.return_value = None
    mock_get_match_status.return_value = "PLAYING"

    response = client.get(f"/status/{str(uuid.uuid4())}")

    assert response.status_code == 200
    assert response.json() == {"status": "PLAYING"}


@patch.object(PostgreSQLRepository, "__init__")
@patch.object(MakeMovementUseCase, "run")
def test_make_valid_move(mock_move, mock_postgre):
    mock_postgre.return_value = None
    mock_move.return_value = "Movement performed. Next turn: O"
    move_data = {
        "matchId": str(uuid.uuid4()),
        "playerId": "X",
        "square": {"x": 0, "y": 0},
    }

    response = client.post("/move", json=move_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Movement performed. Next turn: O"}


# TODO - Next test is causing some issues,
# so I'll continue working on it later on.

# @patch("src.domain.services.match_service.MatchService.move")
# def test_make_invalid_move(mock_move):
#     mock_move.side_effect = HTTPException(
#         status_code=400, detail="Square is not available"
#     )
#     move_data = {
#         "matchId": str(uuid.uuid4()),
#         "playerId": "X",
#         "square": {"x": 0, "y": 0},
#     }

#     # client.post("/move", json=move_data)

#     response = client.post("/move", json=move_data)

#     assert response.status_code == 400  # Se espera un error

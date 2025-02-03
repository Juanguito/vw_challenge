import uuid
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from src.infra.routers import router

client = TestClient(router)


@patch("src.domain.services.match_service.MatchService.create_match")
def test_create_match(mock_create_match):
    mock_create_match.return_value = MagicMock(id=uuid.uuid4(), turn="X")

    response = client.get("/create")

    assert response.status_code == 200
    assert response.json() == {"matchId": str(mock_create_match().id), "turn": "X"}


@patch("src.domain.services.match_service.MatchService.get_match_status")
def test_get_match_status(mock_get_match_status):
    mock_get_match_status.return_value = "PLAYING"

    response = client.get(f"/status/{str(uuid.uuid4())}")

    assert response.status_code == 200
    assert response.json() == {"status": "PLAYING"}


@patch("src.domain.services.match_service.MatchService.move")
def test_make_valid_move(mock_move):
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

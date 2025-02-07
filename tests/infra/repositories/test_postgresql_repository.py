from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.domain.exception.errors import (
    DatabaseGetMatchException,
    DatabaseMatchNotFoundException,
    DatabaseSaveMatchException,
)
from src.domain.models.match import Match
from src.domain.models.status import Status
from src.infra.repositories.postgresql_repository import PostgreSQLRepository


@pytest.fixture
def match():
    return Match(
        id=uuid4(),
        status=Status.PLAYING,
        turn="X",
        board=[
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ],
    )


@pytest.fixture
def repository():
    # configuration extracted from https://docs.sqlalchemy.org/en/20/tutorial/engine.html
    with patch(
        "src.infra.repositories.postgresql_repository.DATABASE_URL",
        "sqlite:///:memory:",
    ):
        logger = MagicMock()
        return PostgreSQLRepository(logger)


def test_save_match_success(match, repository):
    with patch.object(repository, "SessionLocal", return_value=MagicMock()):

        result = repository.save_match(match)
        assert result is not None


def test_save_match_failure(match, repository):
    with patch.object(
        repository, "SessionLocal", side_effect=SQLAlchemyError("DB error")
    ):
        with pytest.raises(DatabaseSaveMatchException):
            repository.save_match(match)


def test_update_match_success(match, repository):
    match_db_mock = MagicMock()
    match_db_mock.to_match.return_value = match

    with patch.object(
        repository, "SessionLocal", return_value=MagicMock()
    ) as mock_session:
        mock_session.execute.return_value.scalar_one_or_none.return_value = (
            match_db_mock
        )

        result = repository.update_match(match)
        assert result is not None


def test_update_match_not_found(match, repository):
    with patch.object(repository, "SessionLocal") as mock_session:
        # I needed help from chatGPT with this mock
        session_instance = mock_session.return_value.__enter__.return_value
        session_instance.execute.return_value.scalar_one_or_none.return_value = None

        with pytest.raises(DatabaseMatchNotFoundException):
            repository.update_match(match)


def test_get_match_success(match, repository):
    match_db = MagicMock()
    match_db.to_match.return_value = match

    with patch.object(
        repository, "SessionLocal", return_value=MagicMock()
    ) as mock_session:
        mock_session.execute.return_value.scalar_one_or_none.return_value = match_db

        result = repository.get_match(match.id)
        assert result is not None


def test_get_match_not_found(repository):
    match_id = uuid4()

    with patch.object(repository, "SessionLocal") as mock_session:
        # I needed help from chatGPT with this mock
        session_instance = mock_session.return_value.__enter__.return_value
        session_instance.execute.return_value.scalar_one_or_none.return_value = None

        result = repository.get_match(match_id)
        assert result is None


def test_get_match_failure(repository):
    match_id = uuid4()

    with patch.object(
        repository, "SessionLocal", side_effect=SQLAlchemyError("DB error")
    ):
        with pytest.raises(DatabaseGetMatchException):
            repository.get_match(match_id)

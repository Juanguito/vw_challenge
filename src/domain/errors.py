from fastapi import HTTPException


class PlayerNotValidException(Exception):
    def __init__(self, message: str):
        self.message = message


class SquareNotValidException(Exception):
    def __init__(self, message: str):
        self.message = message


class MatchAlreadyEndedException(Exception):
    def __init__(self, message: str):
        self.message = message


class TurnNotValidException(Exception):
    def __init__(self, message: str):
        self.message = message


class SquareOutOfBoundsException(Exception):
    def __init__(self, message: str):
        self.message = message


class SquareNotAvailableException(Exception):
    def __init__(self, message: str):
        self.message = message


class MatchNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class DatabaseEnvVarNotSetException(Exception):
    def __init__(self, message: str):
        self.message = message


class DatabaseSaveMatchException(Exception):
    def __init__(self, message: str):
        self.message = message


class DatabaseMatchNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message


class DatabaseUpdateMatchException(Exception):
    def __init__(self, message: str):
        self.message = message


class DatabaseGetMatchException(Exception):
    def __init__(self, message: str):
        self.message = message


def to_http_exception(exception: Exception) -> HTTPException:
    if (
        isinstance(exception, PlayerNotValidException)
        or isinstance(exception, SquareNotValidException)
        or isinstance(exception, MatchAlreadyEndedException)
        or isinstance(exception, TurnNotValidException)
        or isinstance(exception, SquareOutOfBoundsException)
        or isinstance(exception, SquareNotAvailableException)
        or isinstance(exception, DatabaseSaveMatchException)
        or isinstance(exception, DatabaseUpdateMatchException)
        or isinstance(exception, DatabaseGetMatchException)
    ):
        return HTTPException(status_code=400, detail=exception.message)

    if (
        isinstance(exception, MatchNotFoundException)
        or isinstance(exception, DatabaseEnvVarNotSetException)
        or isinstance(exception, DatabaseMatchNotFoundException)
    ):
        return HTTPException(status_code=404, detail=exception.message)

    return HTTPException(status_code=500, detail="Internal server error")

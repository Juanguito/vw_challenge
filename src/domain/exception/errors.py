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

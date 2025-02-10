from typing import Literal

from pydantic import BaseModel


class Square(BaseModel):
    x: int
    y: int


class MovementRequest(BaseModel):
    matchId: str
    playerId: Literal["X", "O", "x", "o"]
    square: Square

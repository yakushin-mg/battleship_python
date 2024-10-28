from enum import Enum


class MoveResult(Enum):
    """Результат хода"""

    MISS = ("miss",)
    DAMAGED = ("damaged",)
    DESTROYED = ("destroyed",)
    WIN = "win"

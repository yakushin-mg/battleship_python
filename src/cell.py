from enum import Enum


class CellType(Enum):
    """Тип клетки"""

    SIMPLE = "simple"
    SHIP = "ship"
    MISS = "miss"
    DAMAGED = "damaged"
    DESTROYED = "destroyed"


class Cell:
    """Клетка поля"""

    __slots__ = ["_type"]
    _type: CellType

    def __init__(self, cell_type: CellType = CellType.SIMPLE) -> None:
        self._type = cell_type

    @property
    def type(self) -> CellType:
        """Тип клетки"""
        return self._type

    @type.setter
    def type(self, value: CellType) -> None:
        self._type = value

    @property
    def is_simple(self) -> bool:
        """Это обычная клетка?"""
        return self.type == CellType.SIMPLE

    @property
    def is_ship(self) -> bool:
        """Это корабль?"""
        return self.type == CellType.SHIP

    def set_ship(self) -> None:
        """Отметка корабля"""
        self.type = CellType.SHIP

    @property
    def is_miss(self) -> bool:
        """Это промах?"""
        return self.type == CellType.MISS

    def set_miss(self) -> None:
        """Отметка промаха."""
        self.type = CellType.MISS

    @property
    def is_damaged(self) -> bool:
        """Это ранение корабля?"""
        return self.type == CellType.DAMAGED

    def set_damaged(self) -> None:
        """Отметка ранения корабля."""
        self.type = CellType.DAMAGED

    @property
    def is_destroyed(self) -> bool:
        """Это потопленный корабль?"""
        return self.type == CellType.DESTROYED

    def set_destroyed(self) -> None:
        """Отметка потопления корабля."""
        self.type = CellType.DESTROYED

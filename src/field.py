from cell import Cell
from move_result import MoveResult
from typing import Set, Tuple, List

DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


class Field:
    """Игровое поле."""

    __slots__ = ["_width", "_length", "_field", "_count_ships"]
    _width: int
    _length: int
    _field: List[List[Cell]]
    _count_ships: int

    def __init__(
        self, width: int = 10, length: int = 10, count_ships: int = 10
    ) -> None:
        self._width = width
        self._length = length
        self._count_ships = count_ships
        self._field = [
            [Cell() for _ in range(length + 1)] for _ in range(width + 1)
        ]

    @property
    def width(self) -> int:
        """Ширина поля"""
        return self._width

    @property
    def length(self) -> int:
        """Длина поля"""
        return self._length

    def __getitem__(self, coords: Tuple[int, int]) -> Cell:
        return self._field[coords[0]][coords[1]]

    def _get_ship_cells(
        self, start_coords: Tuple[int, int]
    ) -> Set[Tuple[int, int]]:
        """Получение всех клеток корабля, у которого есть переданные координаты"""
        ship_cells: Set[Tuple[int, int]] = set()
        ship_cells.add(start_coords)
        for delta_x, delta_y in DIRECTIONS:
            x, y = start_coords
            x += delta_x
            y += delta_y
            while (
                1 <= x <= self.length
                and 1 <= y <= self.width
                and (self[x, y].is_ship or self[x, y].is_damaged)
            ):
                ship_cells.add((x, y))
                x += delta_x
                y += delta_y
        return ship_cells

    def _ship_is_destroyed(self, start_coords: Tuple[int, int]) -> bool:
        """Потоплен ли корабль?"""
        ship_cells = self._get_ship_cells(start_coords)
        for ship_coords in ship_cells:
            if (
                ship_coords != start_coords
                and not self[ship_coords].is_damaged
            ):
                return False
        return True

    def get_result(self, coords: Tuple[int, int]) -> MoveResult:
        """Результат выстрела"""
        result = MoveResult.MISS
        if self[coords].is_ship:
            result = MoveResult.DAMAGED
            if self._ship_is_destroyed(coords):
                result = MoveResult.DESTROYED
                self._count_ships -= 1
                if self._count_ships == 0:
                    result = MoveResult.WIN
        return result

    def update(self, coords: Tuple[int, int], result: MoveResult) -> None:
        """Обновление клетки/клеток после выстрела"""
        if result == MoveResult.MISS:
            self[coords].set_miss()
        elif result == MoveResult.DAMAGED:
            self[coords].set_damaged()
        else:
            ship_cells = self._get_ship_cells(coords)
            for ship_coords in ship_cells:
                self[ship_coords].set_destroyed()

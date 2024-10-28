from connecting import Connection
from console_interface import Console_Interface
from field import Field
from move_result import MoveResult
from random import randint
from typing import Tuple, Set
from user_interface import UserInterface

SHIPS: dict[int, int] = {1: 4, 2: 3, 3: 2, 4: 1}
DIRECTIONS: list[tuple[int, int]] = [
    (0, 0),
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]


class Game:
    """Игра"""

    __slots__ = [
        "_player_field",
        "_enemy_field",
        "_channel",
        "_player_turn",
        "_user_interface",
    ]

    _player_field: Field
    _enemy_field: Field
    _channel: Connection
    _player_turn: bool
    _user_interface: UserInterface

    def __init__(
        self,
        _channel: Connection,
        _player_turn: bool,
        game_type: str = "console",
    ) -> None:
        self._player_field = Field()
        self._enemy_field = Field()
        self._channel = _channel
        self._player_turn = _player_turn
        if game_type == "console":
            self._user_interface = Console_Interface()
        else:
            pass  # TODO: графический интерфейс

    def _place_ship(
        self,
        ship_cells: Set[Tuple[int, int]],
        prohibited_points: Set[Tuple[int, int]],
    ) -> None:
        """Установка корабля"""
        for x, y in ship_cells:
            self._player_field[x, y].set_ship()
            for delta_x, delta_y in DIRECTIONS:
                prohibited_points.add((x + delta_x, y + delta_y))

    def _place_ships(self) -> None:
        """Автоматическое размещение кораблей"""
        prohibited_points: Set[Tuple[int, int]] = set()
        for length, count in SHIPS.items():
            for _ in range(count):
                while True:
                    ship_cells: Set[Tuple[int, int]] = set()
                    x: int = randint(1, self._player_field.width)
                    y: int = randint(1, self._player_field.length)
                    is_horizontal: bool = bool(randint(0, 1))
                    while (
                        len(ship_cells) < length
                        and x <= self._player_field.length
                        and y <= self._player_field.width
                    ):
                        if (x, y) not in prohibited_points:
                            ship_cells.add((x, y))
                        else:
                            ship_cells.clear()
                        if is_horizontal:
                            x += 1
                        else:
                            y += 1
                    if len(ship_cells) == length:
                        self._place_ship(ship_cells, prohibited_points)
                        break

    def _attack(self) -> MoveResult:
        """Атака"""
        coords = self._user_interface.get_coords()
        self._channel.send_move_coords(coords)
        result = self._channel.get_move_result()
        self._enemy_field.update(coords, result)
        return result

    def _defend(self) -> MoveResult:
        """Защита"""
        coords = self._channel.get_move_coords()
        result = self._player_field.get_result(coords)
        self._player_field.update(coords, result)
        self._channel.send_move_result(result)
        return result

    def process(self) -> None:
        """Процесс игры"""
        self._place_ships()
        while True:
            self._user_interface.print_fields(
                self._player_field, self._enemy_field, self._player_turn
            )
            if self._player_turn:
                result = self._attack()
                if result == MoveResult.MISS:
                    self._player_turn = False
                elif result == MoveResult.WIN:
                    is_win: bool = True
                    self._user_interface.end_print_fields(
                        self._player_field, self._enemy_field, is_win
                    )
                    break
            else:
                print("Ожидание выстрела соперника")
                result = self._defend()
                if result == MoveResult.MISS:
                    self._player_turn = True
                elif result == MoveResult.WIN:
                    is_win: bool = False
                    self._user_interface.end_print_fields(
                        self._player_field, self._enemy_field, is_win
                    )
                    break

        del self._user_interface

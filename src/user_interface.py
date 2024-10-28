from abc import ABC, abstractmethod
from typing import Tuple
from field import Field


class UserInterface(ABC):
    @abstractmethod
    def get_coords(self) -> Tuple[int, int]:
        """Получение координат"""
        pass

    @abstractmethod
    def print_fields(
        self, player_field: Field, enemy_field: Field, player_turn: bool
    ) -> None:
        """Вывод полей"""
        pass

    @abstractmethod
    def end_print_fields(
        self, player_field: Field, enemy_field: Field, is_win: bool
    ) -> None:
        """Вывод полей после завершения игры"""
        pass

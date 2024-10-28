from cell import Cell
from field import Field
from os import system
from typing import Tuple, List
from user_interface import UserInterface

COLS_INDEXES = "АБВГДЕЖЗИК"


class Console_Interface(UserInterface):
    def _consol_input(self) -> Tuple[int, int]:
        """Считывание координат и их проверка"""
        try:
            shoot: List[str] = input().split()
            x: int = int(shoot[0])
            y: int = COLS_INDEXES.index(shoot[1]) + 1
        except (ValueError, IndexError) as e:
            raise ValueError from e
        else:
            return x, y

    def get_coords(self) -> Tuple[int, int]:
        """Считывание координат через консоль"""
        while True:
            try:
                print("Введите координаты для выстрела, например 1 А")
                x, y = self._consol_input()
            except ValueError:
                print("Неправильно введены координаты")
            else:
                return x, y

    def _symbol(self, cell: Cell) -> str:
        """Получение символа для клетки"""
        result = " "
        if cell.is_ship:
            result = "■"
        elif cell.is_miss:
            result = "."
        elif cell.is_damaged:
            result = "X"
        elif cell.is_destroyed:
            result = "☠"
        return result

    def _row_field(self, field: Field, row_index: int) -> str:
        """Вывод строки полей через консоль"""
        result: str = str(row_index)
        if row_index <= 9:
            result = " " + result
        result += " |"
        for column in range(1, field.length + 1):
            result += self._symbol(field[row_index, column]) + "|"
        return result

    def print_fields(
        self, player_field: Field, enemy_field: Field, player_turn: bool
    ) -> None:
        """Вывод полей"""
        system("clear")
        print("         Ваше поле         #         Поле соперника")
        print("    А Б В Г Д Е Ж З И К    #       А Б В Г Д Е Ж З И К")
        for row in range(1, player_field.length + 1):
            print(
                self._row_field(player_field, row)
                + "   #   "
                + self._row_field(enemy_field, row)
            )

    def end_print_fields(
        self, player_field: Field, enemy_field: Field, is_win: bool
    ) -> None:
        """Вывод поля после завершения игры"""
        self.print_fields(player_field, enemy_field, True)
        if is_win:
            print("Вы победили!")
        else:
            print("Вы проиграли!")

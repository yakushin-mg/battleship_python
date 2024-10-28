from connecting import Connection, Server, Client
from game import Game
from typing import Union


def init_game() -> None:
    """Инициализация игры."""
    connecting_mode: int = 0
    while connecting_mode not in [1, 2]:
        try:
            print("Выберите режим подключения(введите цифру): \n",
                  "1. Создать сервер\n",
                  "2. Подключиться к серверу")
            connecting_mode = int(input())
        except ValueError:
            print("Введите цифру")

    player_turn: bool = False
    connection: Union[Connection, None] = None

    if connecting_mode == 1:
        connection = Server()
        player_turn = True
    else:
        server_host = input("Введите адрес сервера: ")
        connection = Client(server_host)

    game_type: str = ""
    while game_type not in ["1", "2"]:
        try:
            print("Выберите режим игры: \n",
                  "1. Графический\n",
                  "2. Консольный")
            game_type = input()
        except ValueError:
            print("Введите цифру")

    if game_type == "1":
        game_type = "ui"
    else:
        game_type = "console"

    game = Game(connection, player_turn, game_type)
    game.process()


if __name__ == "__main__":
    init_game()

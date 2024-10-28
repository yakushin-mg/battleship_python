from move_result import MoveResult
from pickle import dumps, loads
from typing import Tuple, Optional
import socket

SIZE = 1024
PORT = 10000


class Connection:
    """Общие методы для сервера и клиента"""

    __slots__ = ["other_person"]
    other_person: Optional[socket.socket]

    def __init__(self) -> None:
        self.other_person = None

    def send_move_coords(self, coords: Tuple[int, int]) -> None:
        """Отправка координат атаки"""
        self.other_person.sendall(dumps(coords))

    def get_move_coords(self) -> Tuple[int, int]:
        """Получение координат атаки"""
        return loads(self.other_person.recv(SIZE))

    def send_move_result(self, result: MoveResult) -> None:
        """Отправка результата атаки"""
        self.other_person.sendall(dumps(result))

    def get_move_result(self) -> MoveResult:
        """Получение результата атаки"""
        return loads(self.other_person.recv(SIZE))

    def __del__(self) -> None:
        """Закрытие соединения"""
        self.other_person.close()


class Client(Connection):
    """Клиент"""

    def __init__(self, host: str) -> None:
        super().__init__()
        self.other_person = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.other_person.connect((host, PORT))

    def __del__(self) -> None:
        super().__del__()


class Server(Connection):
    """Сервер"""

    def __init__(self) -> None:
        super().__init__()
        print("Адрес сервера:", socket.gethostbyname(socket.gethostname()))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), 10000))
        server.listen(1)
        self.other_person, _ = server.accept()

    def __del__(self) -> None:
        super().__del__()

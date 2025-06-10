from copy import deepcopy
from logging import getLogger

logger = getLogger(__name__)


class Operator:
    """Класс-модель, реализующий логику работы с базой данных
        (переменными и их значениями).

    Атрибуты экземпляра (приватные, инициализируются по умолчанию):
        __storage (dict): база данных для переменных и их значений.
        __migration_key (int): ключ для хранения миграций базы данных.
        __migrations (dict): сохранение миграций базы данных
                            (для реализации транзакций).
    """

    def __init__(self) -> None:
        """Инициализирует базу данных для переменных и их значений.
        """
        self.__storage = dict()
        self.__migration_key = 0
        self.__migrations = dict()

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра базы данных.
        """
        return f"Operator(storage={self.__storage}, key={self.__migration_key}, migr={self.__migrations})"

    def set(self, variable: str, value: str) -> None:
        """Сохраняет пару переменная-значение в базу данных.
            Если переменные одинаковые - значение заменяется последним введенным.
            Переменные и значения регистрозависимы.

        Args:
            variable: переменная.
            value: значение переменной.
        """
        self.__storage[variable] = value

    def get(self, variable: str) -> str:
        """Возвращает значение, ранее присвоенное переданной в аргументах
            переменной. Если такой переменной нет в базе данных - возвращает
            NULL.

        Args:
            variable: переменная, значение которой необходимо вернуть.

        Returns:
            значение переменной либо NULL.
        """
        result = self.__storage.get(variable, "NULL")
        return result

    def unset(self, variable: str) -> None:
        """Удаляет из базы данных ранее сохраненную переменную и ее значение.
            Если такой переменной нет - не делает ничего.

        Args:
            variable: переменная для удаления.
        """
        try:
            del self.__storage[variable]
        except KeyError:
            logger.error(f"KeyError in 'unset' method with {variable=}")
            pass

    def counts(self, search_obj: str) -> int:
        """Показывает, сколько раз данное значение встречается в базе данных.

        Args:
            search_obj: значение для поиска в базе данных.

        Returns:
            количество раз, которое данное значение встречается в базе данных.
        """
        counter = 0
        for value in self.__storage.values():
            if value == search_obj:
                counter += 1
        return counter

    def find(self, search_obj: str) -> str:
        """Выводит установленные переменные для переданного
        в аргументе значения.

        Args:
            search_obj: значение для поиска в базе данных.

        Returns:
            переменные, которым установлено значение.
        """
        filtrated = []
        for key, value in self.__storage.items():
            if value == search_obj:
                filtrated.append(key)
        if filtrated:
            result = ", ".join(filtrated)
            return result
        return "NULL"

    def begin(self) -> None:
        """Начинает транзакцию в базе данных.
        """
        logger.info("Start transaction")
        self.__migrations[self.__migration_key] = deepcopy(self.__storage)
        self.__migration_key += 1

    def commit(self) -> None:
        """Сохраняет в базу данных изменения, выполненные в текущей транзакции.
        """
        if self.__migration_key >= 1:
            self.__migration_key -= 1
        if self.__migration_key <= 0:
            self.__migrations.clear()
        logger.info("Transaction has been commited")

    def rollback(self) -> None:
        """Откатывает изменения, выполненные в текущей транзакции.
        """
        if self.__migrations and self.__migration_key >= 1:
            self.__migration_key -= 1
            self.__storage = self.__migrations[self.__migration_key]
            self.__migrations[self.__migration_key] = deepcopy(self.__storage)

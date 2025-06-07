from copy import deepcopy
from logging import getLogger

logger = getLogger(__name__)


class Operator:
    def __init__(self):
        self.__storage = dict()
        self.__migration_key = 0
        self.__migrations = dict()

    def __str__(self):
        return f"Operator(storage={self.__storage}, key={self.__migration_key}, migr={self.__migrations})"

    def set(self, variable: str, value: str) -> None:
        self.__storage[variable] = value

    def get(self, variable: str) -> str:
        result = self.__storage.get(variable, "NULL")
        return result

    def unset(self, variable: str) -> None:
        try:
            del self.__storage[variable]
        except KeyError:
            logger.error(f"KeyError in 'unset' method with {variable=}")
            pass

    def counts(self, search_obj: str) -> int:
        counter = 0
        for value in self.__storage.values():
            if value == search_obj:
                counter += 1
        return counter

    def find(self, search_obj: str) -> str:
        filtrated = []
        for key, value in self.__storage.items():
            if value == search_obj:
                filtrated.append(key)
        if filtrated:
            result = ", ".join(filtrated)
            return result
        return "NULL"

    def begin(self) -> None:
        logger.info("Start transaction")
        self.__migrations[self.__migration_key] = deepcopy(self.__storage)
        self.__migration_key += 1

    def commit(self) -> None:
        self.__migration_key = 0
        self.__migrations.clear()
        logger.info("Transaction has been commited")

    def rollback(self) -> None:
        if self.__migrations:
            self.__migration_key -= 1
            self.__storage = self.__migrations[self.__migration_key]

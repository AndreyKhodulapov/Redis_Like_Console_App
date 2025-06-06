class Operator:
    def __init__(self):
        self.__storage = dict()

    def set(self, variable: str, value: str) -> None:
        self.__storage[variable] = value

    def get(self, variable: str) -> str:
        result = self.__storage.get(variable, "NULL")
        return result

    def unset(self, variable: str) -> None:
        try:
            del self.__storage[variable]
        except KeyError:
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



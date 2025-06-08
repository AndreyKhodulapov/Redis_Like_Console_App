from logging import getLogger, basicConfig, FileHandler, StreamHandler, ERROR, \
    DEBUG

from models import Operator

logger = getLogger()
FORMAT = '%(asctime)s : %(name)s : %(levelname)s: %(message)s'
file_handler = FileHandler("data.log")
file_handler.setLevel(DEBUG)
console = StreamHandler()
console.setLevel(ERROR)
basicConfig(level=DEBUG, format=FORMAT, handlers=[file_handler, console])


def controller(model: Operator, command: str, *args) -> str | None:
    """Осуществляет отклик на команды пользователя.
        Возвращает результат обращения в базе данных.

    Args:
        model: экземпляр базы данных.
        command: команда для базы данных.
        args: аргументы для выполнения команды.

    Returns:
        строка с результатом операции или None.
    """
    commands = {
        "set": model.set,
        "get": model.get,
        "unset": model.unset,
        "counts": model.counts,
        "find": model.find,
        "begin": model.begin,
        "commit": model.commit,
        "rollback": model.rollback,
    }
    try:
        method = commands.get(command, "Incorrect operation")
        if isinstance(method, str):
            return method
        result = method(*args)
        return result
    except Exception as e:
        logger.error(f"Error occurred: {type(e)}: {e}")
        return "Incorrect operation"


def main() -> None:
    """Запускает приложение. Принимает и парсит пользовательский ввод.
        Обеспечивает регистронезависимость команд.
        Останавливает приложение при введении команды "END".

    """
    new_session = Operator()
    while True:
        logger.debug(f"Actual base condition: {new_session}")
        user_input = input(">")
        command, *args = user_input.split()

        logger.info(f"User entered: {command=}, {args=}")

        if command.lower() == "end":
            break

        result = controller(new_session, command.lower(), *args)
        if result is None:
            continue

        print(result)

from models import Operator

def controller(model: Operator, command: str, *args) -> str | None:
    commands = {
        "set": model.set,
        "get": model.get,
        "unset": model.unset,
        "counts": model.counts,
        "find": model.find,
    }
    try:
        method = commands.get(command, "Incorrect operation")
        if isinstance(method, str):
            return method
        result = method(*args)
        return result
    except Exception as e:
        print(e)

def main():
    new_session = Operator()
    while True:
        user_input = input(">")
        command, *args = user_input.split()

        if command.lower() == "end":
            break

        result = controller(new_session, command.lower(), *args)
        if result is None:
            continue

        print(result)
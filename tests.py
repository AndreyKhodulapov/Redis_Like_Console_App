import pytest

from controller import controller
from models import Operator


@pytest.fixture(autouse=True, scope="module")
def create_model():
    model = Operator()
    return model

@pytest.mark.parametrize(
    "args",
    [
        ("get", "A", "NULL"),
        ("set", "A", "1", None),
        ("begin", None),
        ("set", "A", "2", None),
        ("begin", None),
        ("set", "A", "3", None),
        ("commit", None),
        ("get", "A", "3"),
        ("rollback", None),
        ("get", "A", "1"),
        ("unset", "A", None),
    ],
)
def test_transaction_correction(create_model, args):
    command, *arguments, result = args
    assert controller(create_model, command, *arguments) == result

@pytest.mark.parametrize(
    "args",
    [
        ("get", "A", "NULL"),
        ("set", "A", "10", None),
        ("get", "A", "10"),
        ("counts", "10", 1),
        ("set", "B", "20", None),
        ("set", "C", "10", None),
        ("counts", "10", 2),
        ("find", "10", "A, C"),
        ("unset", "A", None),
        ("unset", "B", None),
        ("unset", "C", None),
        ("get", "A", "NULL"),
        ("get", "B", "NULL"),
        ("get", "C", "NULL"),
        ("begin", None),
        ("set", "A", "10", None),
        ("begin", None),
        ("set", "A", "20", None),
        ("begin", None),
        ("set", "A", "30", None),
        ("get", "A", "30"),
        ("rollback", None),
        ("get", "A", "20"),
        ("commit", None),
        ("get", "A", "20"),
    ],
)
def test_app_positive(create_model, args):
    command, *arguments, result = args
    assert controller(create_model, command, *arguments) == result


@pytest.mark.parametrize(
    "args",
    [
        ("no_key",),
        ("",),
        ("no_key", "with", "params"),
        ("get",), ("find",),
        ("set",), ("counts",),
        ("unset",),
        ("get", "more", "params"),
        ("set", "less_params"),
        ("set", "one", "more", "param"),
        ("unset", "more", "params"),
        ("begin", "more", "params"),
        ("commit", "more", "params"),
        ("rollback", "more", "params"),
    ]
)
def test_negative_app(create_model, args):
    command, *arguments = args
    assert controller(create_model, command,
                      *arguments) == "Incorrect operation"

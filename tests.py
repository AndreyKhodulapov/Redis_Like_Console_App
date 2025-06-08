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
        ("set", "A", "10", None),
        ("get", "A", "10"),
        ("counts", "10", 1),
        ("set", "B", "20", None),
        ("set", "C", "10", None),
        ("counts", "10", 2),
        ("find", "10", "A, C"),
        ("unset", "A", None),
        ("get", "A", "NULL"),
        ("set", "A", "5", None),
        ("get", "A", "5"),
        ("begin", None),
        ("set", "A", "10", None),
        ("begin", None),
        ("set", "A", "20", None),
        ("get", "A", "20"),
        ("get", "B", "20"),
        ("unset", "B", None),
        ("get", "B", "NULL"),
        ("rollback", None),
        ("get", "A", "10"),
        ("get", "B", "20"),
        ("rollback", None),
        ("get", "A", "5"),
        ("set", "A", "40", None),
        ("set", "B", "50", None),
        ("commit", None),
        ("get", "A", "40"),
        ("get", "B", "50"),
    ],
)
def test_app_positive(create_model, args):
    command, *arguments, result = args
    assert controller(create_model, command, *arguments) == result


@pytest.mark.parametrize(
    "args",
    [
        ("no_key",),
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

import unittest
from typing import Any

from controller import controller
from models import Operator


class TestController(unittest.TestCase):
    def process_test(self, test_cases: list[tuple], exp_result: Any = None):
        model = Operator()
        for case in test_cases:
            if exp_result is None:
                command, *args, result = case
            else:
                command, *args = case
                result = exp_result
            self.assertEqual(
                controller(model, command, *args),
                result
            )

    def test_set_get(self):
        test_cases = [
            ("get", "A", "NULL"),
            ("set", "A", "10", None),
            ("get", "A", "10"),
        ]

        self.process_test(test_cases)

    def test_counts_find(self):
        test_cases = [
            ("set", "A", "10", None),
            ("counts", "10", 1),
            ("set", "B", "20", None),
            ("set", "C", "10", None),
            ("counts", "10", 2),
        ]

        self.process_test(test_cases)

    def test_set_unset(self):
        test_cases = [
            ("set", "A", "10", None),
            ("get", "A", "10"),
            ("unset", "A", None),
            ("get", "A", "NULL"),
        ]

        self.process_test(test_cases)

    def test_transaction_flow(self):
        test_cases = [
            ("set", "A", "5", None),
            ("get", "A", "5"),
            ("begin", None),
            ("set", "A", "10", None),
            ("begin", None),
            ("set", "A", "20", None),
            ("get", "A", "20"),
            ("rollback", None),
            ("get", "A", "10"),
            ("rollback", None),
            ("get", "A", "5"),
            ("set", "A", "40", None),
            ("set", "B", "50", None),
            ("commit", None),
            ("get", "A", "40"),
            ("get", "B", "50"),
        ]

        self.process_test(test_cases)

    def test_negative(self):
        test_cases = [
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

        self.process_test(test_cases, exp_result="Incorrect operation")


if __name__ == "__main__":
    unittest.main()

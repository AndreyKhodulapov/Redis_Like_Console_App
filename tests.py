import unittest

from controller import controller
from models import Operator

class TestController(unittest.TestCase):
    def test_null_get(self):
        model = Operator()
        self.assertEqual(
            controller(model, "get", "A"),
            "NULL"
        )

    def test_set(self):
        model = Operator()
        self.assertEqual(
            controller(model, "set", "A", "10"),
            None
        )

        self.assertEqual(
            controller(model, "get", "A"),
            "10"
        )

    def test_counts_find(self):
        model = Operator()
        self.assertEqual(
            controller(model, "set", "A", "10"),
            None
        )
        self.assertEqual(
            controller(model, "counts", "10"),
            1
        )
        self.assertEqual(
            controller(model, "set", "B", "20"),
            None
        )
        self.assertEqual(
            controller(model, "set", "C", "10"),
            None
        )
        self.assertEqual(
            controller(model, "counts",  "10"),
            2
        )
        self.assertEqual(
            controller(model, "find", "10"),
            "A, C"
        )

    def set_unset(self):
        model = Operator()
        self.assertEqual(
            controller(model, "set", "A", "10"),
            None
        )
        self.assertEqual(
            controller(model, "get", "A"),
            "10"
        )
        self.assertEqual(
            controller(model, "unset", "A"),
            None
        )
        self.assertEqual(
            controller(model, "get", "A"),
            "NULL"
        )


    #add negative tests!



if __name__ == "__main__":
    unittest.main()
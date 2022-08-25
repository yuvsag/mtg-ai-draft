import unittest
from weight_roller import WeightRoller

WEIGHTS_STUB = {
    "option1": {
        "thing": 3,
        "stuff": 2
    },
    "option2": {
        "thing": 1,
        "stuff": 4
    }
}


class WeightRolling(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def create_roller_and_roll(self, weights_stub):
        roller = WeightRoller(weights_stub)
        return roller.roll()

    def test_gives_the_only_existing_result(self):
        basic_stub = {"option": {"thing": 0.1}}
        result = self.create_roller_and_roll(basic_stub)
        self.assertEqual(result, [["option", "thing"]])

    def test_gives_the_only_result_with_weight(self):
        two_weights_stub = {"option": {"thing": 0, "stuff": 0.1}}
        result = self.create_roller_and_roll(two_weights_stub)
        self.assertEqual(result, [["option", "stuff"]])

    def test_gives_the_result_on_second_option(self):
        two_options_stub = {"option1": {"thing": 0}, "option2": {"thing": 1}}
        result = self.create_roller_and_roll(two_options_stub)
        self.assertEqual(result, [["option2", "thing"]])


if __name__ == "__main__":
    unittest.main()

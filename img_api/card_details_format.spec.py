import unittest

from card_details_format import *


class CardFormatterSpec(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.formatter = CardDetailsFormatter(
            name="generic card name",
            type="Creature", manaCost="{1}",
            power=2, toughness=3,
            text="haste")

    def test_combines_power_and_toughness(self):
        self.assertEqual(
            self.formatter.convert_stats(), "2/3")

    def test_converts_generic_mana_cost(self):
        self.assertEqual(
            self.formatter.convert_mana_symbol("{2}"), "{^^}")

    def test_converts_colored_mana_cost(self):
        self.assertEqual(
            self.formatter.convert_mana_symbol("{2}{R}"), "{^^RR}")

    def test_converts_semi_mana_cost(self):
        self.assertEqual(
            self.formatter.convert_mana_symbol("{2}{R/U}"), "{^^RU}")


if __name__ == "__main__":
    unittest.main()

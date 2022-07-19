import unittest

from card_details_format import CardDetailsFormatter


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
            self.formatter.combine_stats(), "2/3")

    def test_converts_generic_mana_cost(self):
        self.assertEqual(
            self.formatter.combine_mana_symbols("{2}"), "{^^}")

    def test_converts_colored_mana_cost(self):
        self.assertEqual(
            self.formatter.combine_mana_symbols("{2}{R}"), "{^^RR}")

    def test_converts_semi_mana_cost(self):
        self.assertEqual(
            self.formatter.combine_mana_symbols("{2}{R/U}"), "{^^RU}")

    def test_converts_tap_cost(self):
        self.assertEqual(
            self.formatter.combine_mana_symbols("{T}"), "T")

    def test_splits_card_type_single_type(self):
        self.assertEqual(
            self.formatter.split_card_type("Creature"),
            {"type1": "Creature", "type2": "", "subtypes": ""})

    def test_splits_card_type_no_subtypes(self):
        self.assertEqual(
            self.formatter.split_card_type("Artifact Creature"),
            {"type1": "Artifact", "type2": "Creature", "subtypes": ""})

    def test_splits_card_type_with_subtypes(self):
        self.assertEqual(
            self.formatter.split_card_type(
                "Artifact Creature - Goblin Spirit"),
            {"type1": "Artifact", "type2": "Creature", "subtypes": "Goblin Spirit"})


if __name__ == "__main__":
    unittest.main()

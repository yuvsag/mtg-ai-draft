import random

def roll_with_weighs(options: list, weights: list[float], rolls = 1):
    choice = random.choices(
        population=options,
        weights=weights,
        k=rolls
    )
    return list(map(list,choice))


class WeightRoller:
    def __init__(self, weights, weighted_roller=None) -> None:
        self.weighted_roller = weighted_roller or roll_with_weighs
        self.weights = self.expand_weights(weights)

    def expand_weights(self, weights: dict):
        output = {}
        for key, value in weights.items():
            for key2, value2 in value.items():
                output[(key, key2)] = value2
        return output

    def roll(self, num_of_rolls = 1):
        tem = self.weights
        tem_keys = list(tem.keys())
        tem_values = list(tem.values())
        result = self.weighted_roller(tem_keys, tem_values, num_of_rolls)
        return result

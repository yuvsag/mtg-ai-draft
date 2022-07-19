# this class converts from the readable card format
# to the format the image api requires
def int_try_parse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


class CardDetailsFormatter:
    def __init__(self, **kwargs):
        self.card_details = kwargs
        self.card_details_api: dict[str] = {}

    def convert_stats(self):
        power = self.card_details.get('power')
        toughness = self.card_details.get('toughness')
        return f"{power}/{toughness}"

    def convert_mana_symbol(self, mana_cost: str):
        char_list_cost = [c for c in mana_cost if c not in ['{', '}']]
        new_cost = []
        i = -1
        while i < len(char_list_cost) - 1:
            i += 1
            symbol = char_list_cost[i]

            [val, is_int] = int_try_parse(symbol)
            if is_int:
                new_cost.append('^' * val)
                continue

            if symbol == '/':
                new_cost.pop()
                next_symbol = char_list_cost[i+1]
                new_cost.append(next_symbol)
                i += 1
                continue

            new_cost.append(symbol)
            new_cost.append(symbol)
        return f"{{{''.join(new_cost)}}}"

# this class converts from the readable card format
# to the format the image api requires
import re


def int_try_parse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def custom_mana_string_split(mana_string: str):
    arr = re.split(r'(\d+)', mana_string)
    for i, val in enumerate(arr):
        arr[i] = re.sub('[{}]', '', val)
    new_arr = [x for x in arr if x]
    output = []
    appendix = []
    i = -1
    while i < len(new_arr) - 1:
        i += 1
        val = new_arr[i]
        _, is_int = int_try_parse(val)
        if is_int:
            output += appendix
            appendix = []
            output.append(val)
        else:
            appendix += list(val)
    output += appendix
    return output


class CardDetailsFormatter:
    def __init__(self, **kwargs):
        self.card_details = kwargs
        self.card_details_api: dict[str, str] = {}

    def combine_stats(self):
        power = self.card_details.get('power')
        toughness = self.card_details.get('toughness')
        return f"{power}/{toughness}"

    def split_card_type(self, card_type: str):
        split_list = card_type.split(" ")
        output = {}
        output['type1'] = split_list[0]
        output['type2'] = split_list[1] if 1 < len(split_list) else ""
        output['subtypes'] = ""
        if len(split_list) > 3:
            output['subtypes'] = " ".join(split_list[3::])
        return output

    def combine_mana_symbols(self, mana_cost: str):
        char_list_cost = custom_mana_string_split(mana_cost)
        new_cost = []
        i = -1
        while i < len(char_list_cost) - 1:
            i += 1
            symbol = char_list_cost[i]

            if symbol == "T":
                return "T"
            [val, is_int] = int_try_parse(symbol)
            if is_int:
                new_cost.append('^' * val)
                continue

            if symbol == '/':
                popped = new_cost.pop()
                if '^' in popped:
                    # the number itself, not "^^^"
                    new_cost.append(char_list_cost[i-1])
                next_symbol = char_list_cost[i+1]
                new_cost.append(next_symbol)
                i += 1
                continue

            new_cost.append(symbol)
            new_cost.append(symbol)
        return f"{{{''.join(new_cost)}}}"

    def convert_card_text(self, card_text: str):
        new_text = card_text.replace("\n", "\\\\")

        opening_braces = re.finditer("[^}]{|^{", new_text)  # finds opening '{'
        arr1 = [m.span()[1] - 1 for m in opening_braces]  # get their index

        closing_braces = re.finditer("}[^{]|}$", new_text)  # finds closing '}'
        arr2 = [m.span()[0] for m in closing_braces]  # get their index
        braces = list(zip(arr1, arr2))

        old_new = []
        for start, end in braces:
            cost_symbols = new_text[start:end+1]
            new_cost_symbols = self.combine_mana_symbols(cost_symbols)
            old_new.append((cost_symbols, new_cost_symbols))
        for old, new in old_new:
            new_text = new_text.replace(old, new, 1)
        return new_text

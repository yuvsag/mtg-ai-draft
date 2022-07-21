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


def find_all_full_braces(text):
    opening_braces = re.finditer("[^}]{|^{", text)  # finds opening '{'
    arr1 = [m.span()[1] - 1 for m in opening_braces]  # get their index

    closing_braces = re.finditer("}[^{]|}$", text)  # finds closing '}'
    arr2 = [m.span()[0] for m in closing_braces]  # get their index
    braces = list(zip(arr1, arr2))
    return braces


def combine_mana_symbols(mana_cost: str):
    char_list_cost = custom_mana_string_split(mana_cost)
    new_cost = []
    i = -1
    while i < len(char_list_cost) - 1:
        i += 1
        symbol = char_list_cost[i]

        if symbol == "T":
            return "{T}"
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


class CardDetailsFormatter:
    def __init__(self, **kwargs):
        self.card_details = kwargs
        self.card_details_api: dict[str, str] = {}

    def to_api_string(self):
        self.card_details_api["|1"] = self.card_details['name']
        self.card_details_api["|3"] = self.convert_mana_cost()
        card_types = self.split_card_type(self.card_details['type'])
        self.card_details_api["|4"] = card_types["type1"]
        self.card_details_api["|5"] = card_types["type2"]
        self.card_details_api["|6"] = card_types["subtypes"]
        self.card_details_api["|7"] = "rare"  # maybe custom rarity?
        self.card_details_api["|8"] = self.combine_stats()
        self.card_details_api["|9"] = self.convert_card_text(
            self.card_details['text'])

        output = ""
        for key, value in self.card_details_api.items():
            output += key + value
        return output

    def combine_stats(self):
        power = str(self.card_details.get('power', "nan"))
        toughness = str(self.card_details.get('toughness', "nan"))
        if power == "nan" or toughness == "nan":
            return ""
        return f"{power}/{toughness}"

    def convert_mana_cost(self):
        mana_cost = self.card_details.get("manaCost", "")
        if mana_cost != mana_cost:  # a nan check
            return ""
        if mana_cost == "":
            return ""
        return combine_mana_symbols(mana_cost)

    def split_card_type(self, card_type: str):
        split_list = card_type.split(" — ")
        major_types = split_list[0].split(" ")
        output = {}
        output['type1'] = major_types[0]
        output['type2'] = major_types[1] if 1 < len(major_types) else ""
        output['subtypes'] = ""
        if len(split_list) > 1:
            output['subtypes'] = split_list[1]
        return output

    def convert_card_text(self, card_text: str):
        if card_text == "":
            return ""
        new_text = card_text.replace(
            "\n", "\\").replace(
            "\\n", "\\").replace(
            "—", "~").replace(
            "•", "*")

        braces = find_all_full_braces(new_text)
        old_new = []
        for start, end in braces:
            cost_symbols = new_text[start:end+1]
            new_cost_symbols = combine_mana_symbols(cost_symbols)
            old_new.append((cost_symbols, new_cost_symbols))
        for old, new in old_new:
            new_text = new_text.replace(old, new, 1)
        return new_text

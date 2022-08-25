from aitextgen import aitextgen
import pandas as pd

class CardTextGenerator:
    def __init__(self) -> None:
        self.text_gen_ai = aitextgen(model="minimaxir/magic-the-gathering", to_gpu=False)


    def generate_card(self, prompt:str, craziness:float, num_of_cards:int, batch_size:int):
        cards = self.text_gen_ai.generate(n=num_of_cards,
                    batch_size=batch_size,
                    schema=True,
                    prompt=prompt,
                    temperature=craziness,
                    return_as_list=True)

        cards = pd.DataFrame(list(cards))
        cards['text'] = cards.apply(
            lambda row: row['text'].replace("~", row['name']), axis=1)
        cards = cards[['name', 'manaCost', 'type',
        'power', 'toughness','loyalty','text']]
        return cards

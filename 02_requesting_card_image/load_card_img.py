import base64
import os
import requests
import pandas as pd
from card_details_format import CardDetailsFormatter


class ImageGenerator:
    def __init__(self) -> None:
        self.url = os.getenv("LOCAL_API_URL", "http://localhost:8080/")
        self.cards = None

    def generate_img(self, card_details):
        request_text = CardDetailsFormatter(**card_details).to_api_string()
        body = {"text": request_text}
        res = requests.post(self.url, json=body).json()
        img = base64.b64decode(res['image'])
        return img

    def load_cards_from_file(self, file_location: str):
        file_as_df = pd.read_csv(file_location, index_col=0, dtype=str)
        self.cards = file_as_df.to_dict('records')

    def save_all_cards(self, folder_name: str):
        os.mkdir(f"../output/{folder_name}")
        for i, card in enumerate(self.cards):
            img = self.generate_img(card)

            card_file_name = card['name'].replace(
                "//", " ")
            card_file_name = f"({i+1})_{card_file_name}.jpg"

            with open(f"../output/{folder_name}/{card_file_name}", "wb") as file:
                file.write(img)

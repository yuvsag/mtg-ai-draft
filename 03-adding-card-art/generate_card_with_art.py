import os
import io
import re
from glob import glob
import urllib
import requests
from PIL import Image


class ArtGenerator:
    def __init__(self) -> None:
        self.api_url = "https://api.deepai.org/api/text2img"
        self.art_api_key = os.getenv("DEEP_AI_API_KEY")

    def get_art_from_api(self, text_prompt):

        img_request = requests.post(
            self.api_url,
            data={
                'text': text_prompt,
            },
            headers={'api-key': self.art_api_key}
        ).json()
        img_url = img_request['output_url']

        img_res = urllib.request.urlopen(img_url).read()
        img = Image.open(io.BytesIO(img_res))

        w, h = img.size
        img = img.crop((0, 0, w/2, h/2))
        img = img.resize((300, 220))
        return img

    def image_to_bytes(self, image) -> bytes:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

    def put_art_on_card(self, card, art):
        card.paste(art, (35, 65))

    def generate_final_image(self, card_name, file_location):
        card_img = Image.open(file_location)
        card_art = self.get_art_from_api(card_name)
        self.put_art_on_card(card_img, card_art)
        return self.image_to_bytes(card_img)


def get_card_names_from_folder(folder_name):
    image_files = glob(f"../output/{folder_name}/*.jpg")
    image_files.sort(key=os.path.getmtime)
    image_names: list[str] = []
    for card in image_files:
        card_name = card.replace(f'../output/{folder_name}/', '')
        card_name = card_name.replace(".jpg", "")
        card_name = re.sub(r"[\(\[].*?[\)\]]", "", card_name)
        card_name = card_name.replace("_", "")
        image_names.append(card_name)

    return list(zip(image_files, image_names))

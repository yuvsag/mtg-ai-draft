from dataclasses import dataclass


@dataclass(frozen=True)
class TextGenRequest:
    prompt: str = ""
    craziness: int = .7
    numOfCards = 3


@dataclass(frozen=True)
class TextGenResponse:
    name: str
    mana_cost: str
    type: str
    power: str
    toughness: str
    loyalty: str
    text: str

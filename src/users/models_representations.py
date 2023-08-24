from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class Item:
    pk: int
    image_path: str
    price: int


@dataclass
class GraphicsCard(Item):
    income: int


@dataclass
class Character:
    skin: Item
    face: Item | None = None
    haircut: Item | None = None
    clothes: Item | None = None


@dataclass
class User:
    pk: int
    balance: int
    nickname: str
    character: Character
    graphics_cards: Iterable[GraphicsCard]
    status: str
    background_color: str

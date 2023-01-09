from dataclasses import dataclass
from typing import Optional


@dataclass
class AppearanceItem:
    pk: int
    image_path: str
    price: int


@dataclass
class Character:
    skin: AppearanceItem
    face: Optional[AppearanceItem] = None
    haircut: Optional[AppearanceItem] = None
    clothes: Optional[AppearanceItem] = None

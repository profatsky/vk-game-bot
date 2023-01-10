from dataclasses import dataclass


@dataclass
class AppearanceItem:
    pk: int
    image_path: str
    price: int


@dataclass
class Character:
    skin: AppearanceItem
    face: AppearanceItem | None = None
    haircut: AppearanceItem | None = None
    clothes: AppearanceItem | None = None


@dataclass
class User:
    pk: int
    balance: int
    nickname: str
    skin: AppearanceItem
    face: AppearanceItem
    haircut: AppearanceItem
    clothes: AppearanceItem | None
    is_admin: bool

from vkbottle import BaseStateGroup


class RegisterState(BaseStateGroup):
    SKIN = 0
    FACE = 1
    HAIRCUT = 2
    NICKNAME = 3


class ChangeSkin(BaseStateGroup):
    PAGE_1 = 0


class ChangeFace(BaseStateGroup):
    PAGE_1 = 0
    PAGE_2 = 1


class ChangeHaircut(BaseStateGroup):
    PAGE_1 = 0
    PAGE_2 = 1
    PAGE_3 = 2


class ChangeClothes(BaseStateGroup):
    PAGE_1 = 0


class BuyCard(BaseStateGroup):
    BUY = 0


class SellCard(BaseStateGroup):
    SELL = 0


class BlackJack(BaseStateGroup):
    BET = 0
    PROGRESS = 1


class Tsuefa(BaseStateGroup):
    START = 0


class CoinFlip(BaseStateGroup):
    START = 0


class Support(BaseStateGroup):
    ASK = 0


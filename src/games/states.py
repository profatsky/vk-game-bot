from vkbottle import BaseStateGroup


class BlackJackState(BaseStateGroup):
    BET = 0
    GAME = 1


class TsuefaState(BaseStateGroup):
    GAME = 0


class CoinFlipState(BaseStateGroup):
    GAME = 0

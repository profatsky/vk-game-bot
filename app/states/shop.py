from vkbottle import BaseStateGroup


class CharacterShopState(BaseStateGroup):
    CHANGE_SKIN = 0
    CHANGE_FACE = 1
    CHANGE_HAIRCUT = 2
    CHANGE_CLOTHES = 3


class GPUShopState(BaseStateGroup):
    BUY_GPU = 0

from vkbottle import BaseStateGroup


class SupportState(BaseStateGroup):
    QUESTION = 0


class SettingsState(BaseStateGroup):
    NAME = 0
    BACKGROUND = 1

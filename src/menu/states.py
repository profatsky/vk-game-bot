from vkbottle import BaseStateGroup


class ContactSupportState(BaseStateGroup):
    QUESTION = 0


class SettingsState(BaseStateGroup):
    NAME = 0
    BACKGROUND = 1

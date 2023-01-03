from vkbottle.bot import Bot
from vkbottle import CtxStorage

from app import config

bot = Bot(token=config.TOKEN)
ctx = CtxStorage()

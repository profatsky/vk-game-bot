from vkbottle.bot import Bot
from vkbottle import CtxStorage

import config
from database import connector

bot = Bot(token=config.TOKEN)
ctx = CtxStorage()
db = connector.DataBase(
    host=config.host,
    user=config.user,
    db=config.db,
    password=config.password,
    port=3306
)

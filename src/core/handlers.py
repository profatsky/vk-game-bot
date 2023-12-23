from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from users.handlers import start, bl as users_bl
from character_shop.handlers import bl as character_shop_bl
from gpu_shop.handlers import bl as gpu_shop_bl
from menu.handlers import bl as menu_bl
from games.handlers import bl as games_bl
from mining.handlers import bl as mining_bl
from income.handlers import bl as income_bl
from admin.handlers import bl as admin_bl

bl = BotLabeler()


@bl.private_message()
async def unknown_message(message: Message):
    await start(message)


labelers = [
    users_bl,
    menu_bl,
    character_shop_bl,
    gpu_shop_bl,
    mining_bl,
    income_bl,
    games_bl,
    admin_bl,
    bl
]

from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from . import register, main_menu, character_shop, gpu_shop, mining, blackjack, games
from .register import start

bl = BotLabeler()


@bl.private_message()
async def unknown_message(message: Message):
    await start(message)


labelers = [register.bl, character_shop.bl, gpu_shop.bl, mining.bl, blackjack.bl, games.bl, main_menu.bl, bl]

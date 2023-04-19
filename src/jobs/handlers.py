from tortoise.expressions import F
from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from menu.keyboards import income_menu_keyboard
from users.models import UserModel

bl = BotLabeler()


@bl.private_message(payload={'income_menu': 'jobs'})
async def work(message: Message):
    await UserModel.filter(vk_id=message.from_id).update(
        balance=F('balance') + 50,
    )
    await message.answer("💰 Вы заработали $50!", keyboard=income_menu_keyboard)

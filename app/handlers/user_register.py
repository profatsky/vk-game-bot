from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from database.models import User

bl = BotLabeler()


async def is_user_exists(user_id: int):
    return await User.exists(vk_id=user_id)


@bl.private_message(text='Начать')
async def start(message: Message):
    await message.answer('работает')

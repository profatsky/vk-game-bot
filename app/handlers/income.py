from tortoise.expressions import F
from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from database.models import UserModel
from keyboards.income import mining_menu_keyboard, income_menu_keyboard
from .gpu_shop import open_gpu_shop
from .main_menu import show_profile

bl = BotLabeler()


@bl.private_message(payload={'income_menu': 'mining'})
async def open_mining_menu(message: Message):
    user = await UserModel.get(vk_id=message.from_id)
    if not await user.gpu_1 and not await user.gpu_2 and not await user.gpu_3:
        await message.answer(
            "❗ У вас нет видеокарт. "
            "Вы можете купить их в магазине 🏬"
        )
        await open_gpu_shop(message)
    else:
        await show_profile(
            message=message,
            text='📼 Управление видеокартами',
            keyboard=mining_menu_keyboard
        )


@bl.private_message(payload={'income_menu': 'work'})
async def work(message: Message):
    await UserModel.filter(vk_id=message.from_id).update(
        balance=F('balance') + 50,
    )
    await message.answer("💰 Вы заработали $50!", keyboard=income_menu_keyboard)

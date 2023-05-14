from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from config import admin_list, bot
from .keyboards import admin_menu_keyboard

bl = BotLabeler()


@bl.private_message(payload={'menu': 'admin'})
async def open_admin_menu(message: Message):
    await message.answer('🗝 Открываю админ панель', keyboard=admin_menu_keyboard)


@bl.private_message(payload={'admin': 'admin_list'})
async def show_admin_list(message: Message):
    text = '📑 Список администраторов\n\n'
    status_emoji = {'Хелпер': '🦺', 'Администратор': '👔', 'Гл.Администратор': '🎩', 'Основатель': '👑'}
    for vk_id, status in admin_list.storage.items():
        user = (await bot.api.users.get(user_id=vk_id))[0]
        text += f'{status_emoji[status]} {status} - [id{user.id}|{user.first_name} {user.last_name}]\n'
    await message.answer(text, keyboard=admin_menu_keyboard)

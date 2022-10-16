from copy import deepcopy

from vkbottle import PhotoMessageUploader
from vkbottle.bot import Blueprint, Message

from loader import db
from keyboards.menu_kb import main_menu_keyboard, games_menu_keyboard,  income_menu_keyboard, shop_menu_keyboard
from .admin_panel import is_admin
from image_app import create_profile

from vkbottle.tools import Keyboard, KeyboardButtonColor, Text


bp = Blueprint()


@bp.on.private_message(payload={"main_menu": "back"})
async def back_to_menu(message: Message):
    await message.answer("🎈 Главное меню", keyboard=main_menu_keyboard)


# Функция, отвечающая за демонстрацию профиля
@bp.on.private_message(payload={'main_menu': 'profile'})
async def profile(message: Message, text="👤 Ваш профиль", kb=main_menu_keyboard):
    user_info = await db.request(f"SELECT * FROM users WHERE vk_id = {message.from_id}")
    vk_user = (await bp.api.users.get(user_id=user_info['vk_id']))[0]
    if await is_admin(user_info['vk_id']) and kb == main_menu_keyboard:
        kb = deepcopy(main_menu_keyboard)
        kb.row()
        kb.add(Text('🎨 Админ-панель', payload={'admin': 'panel'})).get_json()
    photo = await PhotoMessageUploader(bp.api).upload(await create_profile(user_info, vk_user))
    await bp.api.messages.send(
        peer_id=message.from_id,
        message=text,
        keyboard=kb,
        attachment=photo,
        random_id=0)


# Список игр
@bp.on.private_message(payload={'main_menu': 'games'})
async def games(message: Message):
    await message.answer(f'Список игр', keyboard=games_menu_keyboard)


# Меню магазина
@bp.on.private_message(payload={'choice': 'shop'})
async def shop(message: Message):
    await message.answer(
        '✏ Кастомизация персонажа\n'
        'Покупка атрибутов внешнего вида\n\n'
        '📼 Видеокарты\n'
        'Видеокарты каждый час приносят прибыль. Чем дороже модель видеокарты, тем выше доход',
        keyboard=shop_menu_keyboard
    )


# Список способов заработка
@bp.on.private_message(payload={'main_menu': 'income'})
async def income(message: Message):
    await message.answer(
        'Как заработать 💵?\n\n'
        '💸 Ежедневый бонус\n'
        'Раз в 24 часа можно получить бонус\n'
        'Ежедневный бонус равен 1.000 💵\n\n\n'
        '🖥 Майнинг - фермы:\n'
        'Покупайте видеокарты, которые каждый час приносят прибыль',
        keyboard=income_menu_keyboard
    )

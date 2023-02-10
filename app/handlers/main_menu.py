from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from database.models import UserModel
from images import create_profile_image, convert_image_to_bytes_io
from keyboards.income import income_menu_keyboard
from keyboards.menu import main_menu_keyboard, shop_menu_keyboard, games_menu_keyboard
from utils.vk import upload_image, get_user_name

bl = BotLabeler()


@bl.private_message(payload={"main_menu": "back"})
async def back_to_menu(message: Message):
    await message.answer("🎈 Главное меню", keyboard=main_menu_keyboard)


@bl.private_message(payload={'main_menu': 'profile'})
async def show_profile(
        message: Message,
        text='👤 Ваш профиль',
        keyboard=main_menu_keyboard
):
    user = await UserModel.get(vk_id=message.from_id)
    user = await user.convert_to_dataclass()
    vk_user_name = await get_user_name(message.from_id)
    image = create_profile_image(
        user=user,
        vk_user_name=vk_user_name
    )
    image = await upload_image(convert_image_to_bytes_io(image))
    await message.answer(
        message=text,
        attachment=image,
        keyboard=keyboard
    )


@bl.private_message(payload={'main_menu': 'shop'})
async def show_shop_menu(message: Message):
    await message.answer(
        '✏ Кастомизация персонажа\n'
        'Изменение внешнего вида персонажа\n\n'
        '📼 Видеокарты\n'
        'Видеокарты каждый час приносят прибыль. '
        'Чем дороже модель видеокарты, тем выше доход',
        keyboard=shop_menu_keyboard
    )


@bl.private_message(payload={'main_menu': 'income'})
async def show_income_menu(message: Message):
    await message.answer(
        'Как заработать 💵?\n\n'
        '💸 Ежедневый бонус\n'
        'Раз в 24 часа можно получить бонус\n'
        'Ежедневный бонус равен 1.000 💵\n\n\n'
        '🖥 Майнинг - фермы:\n'
        'Покупайте видеокарты, которые каждый час приносят прибыль',
        keyboard=income_menu_keyboard
    )


@bl.private_message(payload={'main_menu': 'games'})
async def games(message: Message):
    await message.answer(f'Список игр', keyboard=games_menu_keyboard)

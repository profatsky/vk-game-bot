from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from games.keyboards import games_menu_keyboard
from images.gen import create_profile_image, convert_image_to_bytes_io
from images.utils import upload_image
from menu.keyboards import main_menu_keyboard, shop_menu_keyboard, income_menu_keyboard
from users.models import UserModel
from users.utils import get_user_name

bl = BotLabeler()


@bl.private_message(payload={"menu": "back"})
async def back_to_menu(message: Message):
    await message.answer("🎈 Главное меню", keyboard=main_menu_keyboard)


@bl.private_message(payload={'menu': 'profile'})
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


@bl.private_message(payload={'menu': 'shop'})
async def show_shop_menu(message: Message):
    await message.answer(
        '✏ Кастомизация персонажа\n'
        'Изменение внешнего вида персонажа\n\n'
        '📼 Видеокарты\n'
        'Видеокарты каждый час приносят прибыль.'
        'Чем дороже модель видеокарты, тем выше доход',
        keyboard=shop_menu_keyboard
    )


@bl.private_message(payload={'menu': 'income'})
async def show_income_menu(message: Message):
    await message.answer(
        'Как заработать 💵?\n\n'
        '💸 Ежедневный бонус\n'
        'Раз в сутки получайте денежный бонус!\n\n\n'
        '🔨 Работа\n'
        'Нажимайте на кнопку - получайте деньги!\n\n\n'
        '🖥 Майнинг - фермы:\n'
        'Покупайте видеокарты, которые каждый час приносят прибыль!',
        keyboard=income_menu_keyboard
    )


@bl.private_message(payload={'menu': 'games'})
async def games(message: Message):
    await message.answer(f'Список игр', keyboard=games_menu_keyboard)

from datetime import datetime

from tortoise.expressions import F
from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler
from vkbottle.modules import json

from config import bot
from images import upload_image
from menu.handlers import show_shop_menu, show_profile
from mining.keyboards import mining_menu_keyboard
from mining.models import MiningModel
from users.models import GraphicsCardModel, UserModel
from users.utils import get_free_gpu_slot, is_enough_money
from .keyboards import gpu_shop_keyboard
from .states import GPUShopState

bl = BotLabeler()


@bl.private_message(payload={'shop_menu': 'gpu'})
async def open_gpu_shop(message: Message):
    image = await upload_image('assets/img/gpu_shop.png')
    await message.answer(
        message='📼 Видеокарты доступные для покупки\n\n❗ '
                'Каждый пользователь может владеть лишь 3 видеокартами',
        attachment=image,
        keyboard=gpu_shop_keyboard
    )
    await bot.state_dispenser.set(message.peer_id, GPUShopState.BUY_GPU)


@bl.private_message(state=GPUShopState.BUY_GPU)
async def buy_gpu(message: Message):
    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=gpu_shop_keyboard
        )

    choice = json.loads(message.payload)['choice']
    if choice == 'back_to_shop':
        await bot.state_dispenser.delete(message.from_id)
        await show_shop_menu(message)
    else:
        free_slot = await get_free_gpu_slot(message.from_id)
        if not free_slot:
            await bot.state_dispenser.delete(message.from_id)
            return await show_profile(
                message=message,
                text='❗ Вы уже владеете максимальным количеством видеокарт',
                keyboard=mining_menu_keyboard
            )
        chosen_gpu = await GraphicsCardModel.get(pk=choice)
        if await is_enough_money(message.from_id, chosen_gpu.price):
            await UserModel.filter(vk_id=message.from_id).update(
                balance=F('balance') - chosen_gpu.price, **{f'{free_slot}_id': choice},
            )
            user = await UserModel.get(vk_id=message.from_id)
            await MiningModel.update_or_create(
                user_id=user.pk,
                defaults={free_slot: datetime.utcnow()}
            )
            await show_profile(
                message,
                text=f'🥳 Вы приобрели видеокарту за ${chosen_gpu.price}',
                keyboard=gpu_shop_keyboard
            )
        else:
            await message.answer('❗ У вас недостаточно средств!')

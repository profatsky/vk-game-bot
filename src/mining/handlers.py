from datetime import datetime, timedelta

from tortoise.expressions import F
from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler
from vkbottle.modules import json

from core.loader import bot
from gpu_shop.handlers import open_gpu_shop
from gpu_shop.states import GPUShopState
from menu.handlers import show_profile
from users.models import UserModel
from .keyboards import mining_menu_keyboard
from .models import MiningModel
from .utils import generate_sell_gpu_keyboard

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


@bl.private_message(payload={'mining_menu': 'get_income'})
async def get_mining_income(message: Message):
    user = await UserModel.get(vk_id=message.from_id)
    mining = await MiningModel.get(user_id=user.pk)

    total_income = 0
    message_text = ''
    update_mining_fields = []

    for i in range(1, 4):
        gpu_field_name = f'gpu_{i}'
        if getattr(mining, gpu_field_name):
            mining_time = datetime.utcnow() - getattr(mining, gpu_field_name).replace(tzinfo=None)
            hours = int(mining_time / timedelta(hours=1))
            income = hours * (await getattr(user, gpu_field_name)).income
            if income:
                total_income += income
                # Оставшиеся минуты за вычетом часов работы видеокарты
                remaining_minutes = (mining_time - timedelta(hours=hours)) / timedelta(minutes=1)
                new_start_time = datetime.utcnow() - timedelta(minutes=remaining_minutes)
                setattr(mining, gpu_field_name, new_start_time)
                update_mining_fields.append(gpu_field_name)
                message_text += f'✔ {i}-я видеокарта принесла ${income} дохода\n'
            else:
                message_text += f'❌ {i}-я видеокарта не принесла дохода\n'

    await mining.save(update_fields=update_mining_fields)
    user.balance = F('balance') + total_income
    await user.save(update_fields=['balance'])

    await message.answer(
        f'💰 Общий доход от майнинга составил ${total_income}\n\n'
        f'{message_text}'
    )


@bl.private_message(payload={'mining_menu': 'sell_cards'})
async def open_sell_gpu_menu(message: Message):
    user = await UserModel.get(vk_id=message.from_id)

    cards_numbers = []
    for i in range(1, 4):
        if await getattr(user, f'gpu_{i}'):
            cards_numbers.append(i)

    keyboard = generate_sell_gpu_keyboard(cards_numbers)

    await show_profile(
        message=message,
        text='📼 Выберите видеокарту, которую хотите продать',
        keyboard=keyboard
    )
    await bot.state_dispenser.set(
        peer_id=message.from_id,
        state=GPUShopState.SELL_GPU,
        keyboard=keyboard
    )


@bl.private_message(state=GPUShopState.SELL_GPU)
async def sell_gpu(message: Message):
    state_payload = message.state_peer.payload

    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=state_payload['keyboard']
        )

    choice = json.loads(message.payload)['choice']
    if choice == 'back':
        await open_mining_menu(message)
        await bot.state_dispenser.delete(message.from_id)
    else:
        gpu_field_name = f'gpu_{choice}'
        user = await UserModel.get(vk_id=message.from_id)
        gpu = await getattr(user, gpu_field_name)
        gpu_selling_price = int(gpu.price / 2)
        setattr(user, gpu_field_name, None)
        user.balance = F('balance') + gpu_selling_price
        await user.save(update_fields=['balance', f'{gpu_field_name}_id'])
        await MiningModel.filter(user_id=user.pk).update(
            **{gpu_field_name: None}
        )

        await show_profile(
            message=message,
            text=f'✔ Вы продали видеокарту за ${gpu_selling_price}',
            keyboard=mining_menu_keyboard
        )
        await bot.state_dispenser.delete(message.from_id)

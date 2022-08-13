import json
from datetime import datetime, timedelta

from vkbottle.bot import Blueprint, Message
from vkbottle.tools import Keyboard, Text

from loader import db
from blueprints.main_menu import profile
from blueprints.shop import mining_shop
from keyboards import income_kb
from states import SellCard

bp = Blueprint()


# Демонстрация видеокарт пользователя
@bp.on.private_message(payload={'income_menu': 'mining'})
async def mining_menu(message: Message):
    if await db.request(f"SELECT * FROM mining "
                        f"WHERE user_id = (SELECT user_id FROM users WHERE vk_id = {message.from_id})", "result"):
        await profile(
            message=message,
            text='📼 Ваши видеокарты',
            kb=income_kb.mining_keyboard
        )
    else:
        await message.answer("❗ У вас нет видеокарт. Вы можете купить их в магазине 🏬")
        await mining_shop(message)


# Получени прибыли от видеокарты
async def get_card_income(message: Message, video_card: str, cards_amount: int):
    start_mining_date = (await db.request(
        f"SELECT low_card, medium_card, high_card FROM mining "
        f"WHERE user_id = (SELECT user_id FROM users WHERE vk_id = {message.from_id})"))[video_card]

    # Узнаем сколько времени карта майнила
    mining_time = datetime.now() - start_mining_date
    # Узнаем сколько часов карта майнила
    number_of_hours = int(mining_time / timedelta(hours=1))
    # Узнаем доход от видеокарты указанной модели
    income_from = {"low_card": 25, "medium_card": 80, "high_card": 250}
    income_from_the_card = number_of_hours * income_from[video_card] * cards_amount
    if income_from_the_card:
        # Сколько минут карта проработала после вычета часов
        remaining_minutes = (mining_time - timedelta(hours=number_of_hours)) / timedelta(minutes=1)
        # Уменьшаем время начала работы видеокарты
        start_time = datetime.now() - timedelta(minutes=remaining_minutes)
        await db.request(f'UPDATE mining SET {video_card} = "{start_time}" '
                         f'WHERE user_id = (SELECT user_id FROM users WHERE vk_id = {message.from_id})')
        await message.answer(
            f"Доход от ведеокарт(ы) «{video_card.split('_')[0].capitalize()}» составил ${income_from_the_card}"
        )
    else:
        await message.answer(f"❌ Видеокарта(-ы) «{video_card.split('_')[0].capitalize()}» не принесла(-и) дохода")
    return income_from_the_card


# Получение прибыли
@bp.on.private_message(payload={'mining_menu': 'get_income'})
async def get_mining_income(message: Message):
    slots = await db.request(f"SELECT slot_1, slot_2, slot_3 FROM users WHERE vk_id = {message.from_id}")
    no_cards_amount = sum(map(lambda card: card == "no_card", slots.values()))
    general_income = 0
    if no_cards_amount != 3:
        low_cards_amount = sum(map(lambda card: card == "low_card", slots.values()))
        if low_cards_amount:
            # Получение прибыли от видеокарт категории Low
            income_from_low = await get_card_income(
                message=message,
                video_card="low_card",
                cards_amount=low_cards_amount
            )
            general_income += income_from_low

        medium_cards_amount = sum(map(lambda card: card == "medium_card", slots.values()))
        if medium_cards_amount:
            # Получение прибыли от видеокарт категории Medium
            income_from_medium = await get_card_income(
                message=message,
                video_card="medium_card",
                cards_amount=medium_cards_amount
            )
            general_income += income_from_medium

        high_cards_amount = sum(map(lambda card: card == "high_card", slots.values()))
        if high_cards_amount:
            # Получение прибыли от видеокарт категории High
            income_from_high = await get_card_income(
                message=message,
                video_card="high_card",
                cards_amount=high_cards_amount
            )
            general_income += income_from_high

        await db.request(f"UPDATE users SET balance = balance + {general_income} WHERE vk_id = {message.from_id}")
        await message.answer(f"Общий доход от видеокарт составил ${general_income}")
    else:
        await message.answer("❗ У вас нет видеокарт. Вы можете купить их в магазине 🏬")
        await mining_shop(message)


# Продажа видеокарты
@bp.on.private_message(payload={'mining_menu': 'sell_cards'})
async def sell_video_card_menu(message: Message):
    slots = await db.request(f"SELECT slot_1, slot_2, slot_3 FROM users WHERE vk_id = {message.from_id}")
    cards_list = {"low_card": 750, "medium_card": 3750, "high_card": 12500}  # стоимость продажи каждой из видеокарт

    # Получение списка видеокарт доступных для продажи
    text = ""
    kb = Keyboard(one_time=False, inline=False)
    count = 1
    for slot, card in slots.items():
        if card != "no_card":
            text += f"{count}. {card.split('_')[0].capitalize()} - ${cards_list[card]}\n"
            kb.add(Text(
                f"{count}. {card.split('_')[0].capitalize()}",
                payload={"sell_cards": (slot, card, cards_list[card])}
            ))
            count += 1

    if text:
        kb.row().add(Text("❌ Отказаться от продажи", payload={"sell_cards": "refuse"}))
        await message.answer(f"🖥 Список видеокарт доступных для продажи:\n\n{text}", keyboard=kb.get_json())
        await bp.state_dispenser.set(peer_id=message.peer_id, state=SellCard.SELL)
    else:
        await message.answer("❗ У вас нет видеокарт. Вы можете купить их в магазине 🏬")
        await mining_shop(message)


@bp.on.private_message(state=SellCard.SELL)
async def sell_video_card(message: Message):
    if message.payload:
        answer = json.loads(message.payload)["sell_cards"]
        if answer == "refuse":  # если пользователь отказался от продажи видеокарты
            await message.answer("Вы отказались от продажи видеокарты")
            await bp.state_dispenser.delete(peer_id=message.peer_id)
            await mining_menu(message)
        else:
            slot, card_name, money = answer
            await db.request(
                f'UPDATE users JOIN mining USING (user_id) '
                f'SET balance = balance + {money}, users.{slot} = "no_card", mining.{card_name} = NULL '
                f'WHERE vk_id = {message.from_id}'
            )
            await message.answer(f"💰 Вы продали видеокарту {card_name.split('_')[0].capitalize()} за ${money}")
            await bp.state_dispenser.delete(peer_id=message.peer_id)
            await mining_menu(message)
    else:
        await message.answer("❗ Нажмите на кнопку!")

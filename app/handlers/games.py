import random

from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler
from vkbottle.modules import json

from config import bot
from keyboards.games import tsuefa_keyboard, coin_flip_keyboard
from keyboards.menu import games_menu_keyboard
from states.games import TsuefaState, CoinFlipState

bl = BotLabeler()


@bl.private_message(payload={'games': 'tsuefa'})
async def start_tsuefa_game(message: Message):
    await bot.state_dispenser.set(message.peer_id, TsuefaState.GAME)
    await message.answer(
        'Камень, ножницы, бумага. Цу-е-фа!',
        keyboard=tsuefa_keyboard
    )


@bl.private_message(state=TsuefaState.GAME)
async def play_tsuefa_game(message: Message):
    if not message.payload:
        return await message.answer(
            '❗ Некорректный ввод',
            keyboard=tsuefa_keyboard
        )
    keyboard = games_menu_keyboard
    player_sign = json.loads(message.payload)['tsuefa']
    bot_sign = {1: 'Камень', 2: 'Ножницы', 3: 'Бумага'}[random.randint(1, 3)]
    if player_sign == 'Камень':
        if bot_sign == 'Камень':
            await message.answer('👊Камень! Ничья 😏', keyboard=keyboard)
        elif bot_sign == 'Ножницы':
            await message.answer('✌Ножницы! Вы выиграли 😉', keyboard=keyboard)
        elif bot_sign == 'Бумага':
            await message.answer('✋Бумага! Вы проиграли 😕', keyboard=keyboard)
    elif player_sign == 'Ножницы':
        if bot_sign == 'Камень':
            await message.answer('👊Камень! Вы проиграли 😕', keyboard=keyboard)
        elif bot_sign == 'Ножницы':
            await message.answer('✌Ножницы! Ничья 😏', keyboard=keyboard)
        elif bot_sign == 'Бумага':
            await message.answer('✋Бумага! Вы выиграли 😉', keyboard=keyboard)
    elif player_sign == 'Бумага':
        if bot_sign == 'Камень':
            await message.answer('👊Камень! Вы выиграли 😉', keyboard=keyboard)
        elif bot_sign == 'Ножницы':
            await message.answer('✌Ножницы! Вы проиграли 😕', keyboard=keyboard)
        elif bot_sign == 'Бумага':
            await message.answer('✋Бумага! Ничья 😏', keyboard=keyboard)
    elif player_sign == '◀ К списку игр':
        await message.answer('Список игр', keyboard=keyboard)
    await bot.state_dispenser.delete(message.peer_id)


@bl.private_message(payload={'games': 'coinflip'})
async def start_coin_flip(message: Message):
    await bot.state_dispenser.set(message.peer_id, CoinFlipState.GAME)
    await message.answer('Игра «Монетка»', keyboard=coin_flip_keyboard)


@bl.private_message(state=CoinFlipState.GAME)
async def coin_flip_game(message: Message):
    if not message.payload:
        return await message.answer(
            '❗ Некорректный ввод',
            keyboard=coin_flip_keyboard
        )
    answer = json.loads(message.payload)['coin_flip']
    if message.payload == 'back':
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(
            'Список игр',
            keyboard=games_menu_keyboard
        )
    else:
        another_side = 'Решка' if answer == 'Орел' else 'Орел'
        if random.randint(1, 2) == 1:
            await message.answer(
                f'🥳 {answer}! Вы выиграли!',
                keyboard=games_menu_keyboard)
        else:
            await message.answer(
                f'😕 {another_side}! Вы проиграли',
                keyboard=games_menu_keyboard
            )
        await bot.state_dispenser.delete(message.peer_id)

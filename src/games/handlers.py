import random
from dataclasses import dataclass

from tortoise.expressions import F
from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler
from vkbottle.modules import json

from config import bot
from games.keyboards import tsuefa_keyboard, coin_flip_keyboard, games_menu_keyboard, blackjack_action_keyboard, \
    bet_keyboard
from games.states import TsuefaState, CoinFlipState, BlackJackState
from users.models import UserModel
from users.utils import is_enough_money, get_user_balance

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


@dataclass
class BlackJackCard:
    title: str
    score: int
    suit: str = None

    def __str__(self):
        return f"{self.title} {self.suit}"


@bl.private_message(payload={'games': 'blackjack'})
async def start_blackjack_game(message: Message):
    balance = await get_user_balance(vk_id=message.from_id)

    await message.answer(
        message=f'🎮 Игра Blackjack🃏\n'
                f'💵 Ваш баланс: ${balance}\n'
                f'✏ Введите сумму ставки',
        keyboard=bet_keyboard
    )
    await bot.state_dispenser.set(
        peer_id=message.from_id,
        state=BlackJackState.BET
    )


@bl.private_message(state=BlackJackState.BET, text='<answer>')
async def place_bet_blackjack_game(message: Message, answer=None):
    if answer == '◀ К списку игр':
        await message.answer(f'🎮 Список игр', keyboard=games_menu_keyboard)
        await bot.state_dispenser.delete(message.from_id)
    elif answer == 'Без ставки':
        await play_blackjack_game(message)
    elif answer.isdigit():
        bet_amount = int(answer)
        if not await is_enough_money(message.from_id, bet_amount):
            await message.answer(
                message='У вас недостаточно средств',
                keyboard=bet_keyboard
            )
        else:
            await UserModel.filter(vk_id=message.from_id).update(
                balance=F('balance') - bet_amount
            )
            await message.answer(f'💰 Ваша ставка {bet_amount}')
            await play_blackjack_game(message, bet_amount)


async def play_blackjack_game(message: Message, bet_amount: int = 0):
    player_hand = []
    player_score = 0
    dealer_hand = []
    dealer_score = 0

    for i in range(2):
        card = get_card(player_hand)
        player_hand.append(card)
        player_score += card.score

    card = get_card(dealer_hand + player_hand)
    dealer_hand.append(card)
    dealer_score += card.score

    await message.answer(
        f'🙋‍♂Ваши карты:\n{player_hand[0]}, {player_hand[1]}\n'
        f'Счет: {player_score}\n\n'
        f'🤵Карты Крупье:\n{dealer_hand[0]}\n'
        f'Счет: {dealer_score}'
    )

    if player_score >= 21:
        await UserModel.filter(vk_id=message.from_id).update(
            balance=F('balance') + 2 * bet_amount
        )
        await bot.state_dispenser.delete(message.from_id)
        await message.answer(
            '🙆‍♂️Блэкджек! Победа!\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    else:
        await message.answer(
            '➕ Еще - взять карту\n⛔ СТОП - завершить игру и узнать результат',
            keyboard=blackjack_action_keyboard
        )
        await bot.state_dispenser.set(
            message.peer_id,
            BlackJackState.GAME,
            player_hand=player_hand,
            player_score=player_score,
            dealer_hand=dealer_hand,
            dealer_score=dealer_score,
            bet_amount=bet_amount
        )


@bl.private_message(state=BlackJackState.GAME, payload={'blackjack': 'take_more'})
async def take_more(message: Message):
    state_payload = message.state_peer.payload

    card = get_card(state_payload['player_hand'] + state_payload['dealer_hand'])
    state_payload['player_hand'].append(card)
    state_payload['player_score'] += card.score

    await message.answer(
        f'🙋‍♂Ваши карты:\n'
        f'{", ".join([str(card) for card in state_payload["player_hand"]])}\n'
        f'Счет: {state_payload["player_score"]}\n\n'
        f'🤵Карты Крупье:\n'
        f'{state_payload["dealer_hand"][0]}\n'
        f'Счет: {state_payload["dealer_score"]}'
    )

    if state_payload['player_score'] == 21:
        await UserModel.filter(vk_id=message.from_id).update(
            balance=F('balance') + 2 * state_payload['bet_amount']
        )
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(
            '🙆‍♂️Блэкджек! Победа!\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    elif state_payload['player_score'] > 21:
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(
            f'🤦‍♂️Много! Вы проиграли!\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    else:
        await message.answer(
            '➕ Еще - взять карту\n⛔ СТОП - завершить игру и узнать результат',
            keyboard=blackjack_action_keyboard
        )


@bl.private_message(state=BlackJackState.GAME, payload={'blackjack': 'stop_game'})
async def stop_blackjack_game(message: Message):
    state_payload = message.state_peer.payload

    while state_payload['dealer_score'] < 17:
        card = get_card(state_payload['player_hand'] + state_payload['dealer_hand'])
        state_payload['dealer_hand'].append(card)
        state_payload['dealer_score'] += card.score

    await message.answer(
        f"🙋‍♂Ваши карты:\n"
        f"{', '.join([str(card) for card in state_payload['player_hand']])}\n"
        f"Счет: {state_payload['player_score']}\n\n"
        f"🤵Карты Крупье:\n"
        f"{', '.join([str(card) for card in state_payload['dealer_hand']])}\n"
        f"Счет: {state_payload['dealer_score']}"
    )

    if state_payload['dealer_score'] > 21 or state_payload['player_score'] > state_payload['dealer_score']:
        await UserModel.filter(vk_id=message.from_id).update(
            balance=F('balance') + 2 * state_payload['bet_amount']
        )
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(
            '🙆‍♂️Поздравляю! Победа!\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    elif state_payload['dealer_score'] == state_payload['player_score']:
        await UserModel.filter(vk_id=message.from_id).update(
            balance=F('balance') + state_payload['bet_amount']
        )
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(
            '💁‍♂️Пуш! Ничья\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    else:
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(
            '🤦‍♂️К сожалению, вы проиграли\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )


@bl.private_message(state=BlackJackState.GAME)
async def incorrect_message_during_game(message: Message):
    await message.answer(
        '❗ Некорректный ввод!',
        keyboard=blackjack_action_keyboard
    )


def get_card(current_cards: list):
    print(current_cards)
    while True:
        card_num = random.randint(2, 14)
        card_suit = random.randint(1, 4)

        if card_num == 11:
            card = BlackJackCard(
                title='Валет',
                score=10
            )
        elif card_num == 12:
            card = BlackJackCard(
                title='Дама',
                score=10
            )
        elif card_num == 13:
            card = BlackJackCard(
                title='Король',
                score=10
            )
        elif card_num == 14:
            card = BlackJackCard(
                title='Туз',
                score=11
            )
        else:
            card = BlackJackCard(
                title=str(card_num),
                score=card_num
            )

        suits = {1: '♣', 2: '♥', 3: '♦', 4: '♠'}
        card.suit = suits[card_suit]

        if card in current_cards:
            continue
        break

    return card

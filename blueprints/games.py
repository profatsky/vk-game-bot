import json
import random

from vkbottle.bot import Blueprint, Message

from loader import db, ctx
from blueprints.shop import check_balance
from keyboards import games_kb
from keyboards.menu_kb import games_menu_keyboard
from states import BlackJack, Tsuefa, CoinFlip

bp = Blueprint()


# Игра "Блэкджек"
@bp.on.private_message(payload={'games': 'blackjack'})
async def start_blackjack(message: Message):
    balance = f"{await check_balance(message.from_id):,}".replace(",", ".")
    await message.answer(
        f'Игра Blackjack🃏\n'
        f'Ваш баланс: ${balance} 💵\n'
        f'Введите сумму ставки',
        keyboard=games_kb.bet_keyboard
    )
    await bp.state_dispenser.set(message.peer_id, BlackJack.BET)


@bp.on.private_message(state=BlackJack.BET, text="<answer>")
async def bet_blackjack(message: Message, answer=None):
    if answer == '◀ К списку игр':
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(f'🎮 Список игр', keyboard=games_menu_keyboard)
    elif answer == 'Без ставки':
        await blackjack(message)
    else:
        # Если пользователь ввел число
        if answer.isdigit():
            # Проверка, достаточно ли средств на балансе
            balance = await check_balance(message.from_id)
            answer = int(answer)
            if balance < answer:
                await message.answer(f'❗ У вас недостаточно средств!')
            else:
                # Списание средств и начало игры
                ctx.set("bet", answer)
                await db.request(f"UPDATE users SET balance = balance - {answer} WHERE vk_id = {message.from_id}")
                await message.answer(f'Ваша ставка: {answer} 💵')
                await blackjack(message)
        else:
            await message.answer(f'❗ Некорректный ввод', keyboard=games_kb.bet_keyboard)


async def get_card(hand: list):
    while True:
        card_num = random.randint(2, 14)  # выбор карты
        card_suit = random.randint(1, 4)  # выбор масти

        # Сохранение названия карты и её номинала
        if card_num == 11:
            card = 'Валет'
            score = 10
        elif card_num == 12:
            card = 'Дама'
            score = 10
        elif card_num == 13:
            card = 'Король'
            score = 10
        elif card_num == 14:
            card = 'Туз'
            score = 11
        else:
            card = str(card_num)
            score = card_num

        # Сохранение масти в виде эмодзи
        suits = {1: ' ♣', 2: ' ♥', 3: ' ♦', 4: ' ♠'}
        card += suits[card_suit]

        if card in hand:  # выбор новой карты, если такая уже была разыграна
            continue
        break

    return card, score


# Начало игры в блэкджек, первая раздача карт
async def blackjack(message: Message):
    player_hand = []
    player_score = 0
    dealer_hand = []
    dealer_score = 0

    # Первая карта игрока
    card_info = await get_card(hand=[])
    player_hand.append(card_info[0])
    player_score += card_info[1]

    # Вторая карта игра
    card_info = await get_card(player_hand)
    player_hand.append(card_info[0])
    player_score += card_info[1]

    # Первая карта диллера
    card_info = await get_card(dealer_hand)
    dealer_hand.append(card_info[0])
    dealer_score += card_info[1]

    # Сохранение данных в CtxStorage
    ctx.set("player_hand", player_hand)
    ctx.set("player_score", player_score)
    ctx.set("dealer_hand", dealer_hand)
    ctx.set("dealer_score", dealer_score)

    await message.answer(
        f"🙋‍♂Ваши карты:\n"
        f"{player_hand[0]}, {player_hand[1]}\n"
        f"Счет: {player_score}\n\n"
        f"🤵Карты Крупье:\n"
        f"{dealer_hand[0]}\n"
        f"Счет: {dealer_score}"
    )

    if player_score >= 21:
        await db.request(f"UPDATE users SET balance = balance + {ctx.get('bet')} * 2 WHERE vk_id = {message.from_id}")
        ctx.storage.clear()
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(
            '🙆‍♂️Блэкджек! Победа!\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    else:
        await message.answer(
            '➕ Еще - взять карту\n⛔ СТОП - завершить игру и узнать результат',
            keyboard=games_kb.blackjack_keyboard
        )
        await bp.state_dispenser.set(message.peer_id, BlackJack.PROGRESS)


# Если игрок берет еще одну карту при игре в Блэкджек
@bp.on.private_message(state=BlackJack.PROGRESS, payload={"blackjack": "more"})
async def take_more(message: Message):
    # Получение данных о текущей игре
    player_hand = ctx.get("player_hand")
    player_score = ctx.get("player_score")
    dealer_hand = ctx.get("dealer_hand")
    dealer_score = ctx.get("dealer_score")

    # Игрок получает новую карту
    card_info = await get_card(hand=player_hand + dealer_hand)
    player_hand.append(card_info[0])
    player_score += card_info[1]

    # Сохранение данных о текущей игре
    ctx.set("player_hand", player_hand)
    ctx.set("player_score", player_score)

    await message.answer(
        f"🙋‍♂Ваши карты:\n"
        f"{', '.join(player_hand)}\n"
        f"Счет: {player_score}\n\n"
        f"🤵Карты Крупье:\n"
        f"{dealer_hand[0]}\n"
        f"Счет: {dealer_score}"
    )

    if player_score == 21:
        await db.request(f"UPDATE users SET balance = balance + {ctx.get('bet')} * 2 WHERE vk_id = {message.from_id}")
        ctx.storage.clear()
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(
            '🙆‍♂️Блэкджек! Победа!\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    elif player_score > 21:
        ctx.storage.clear()
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(
            f'🤦‍♂️Много! Вы проиграли!\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    else:
        await message.answer(
            '➕ Еще - взять карту\n⛔ СТОП - завершить игру и узнать результат',
            keyboard=games_kb.blackjack_keyboard
        )


# Если игрок решил закончить игру в Блэкджек
@bp.on.private_message(state=BlackJack.PROGRESS, payload={"blackjack": "stop"})
async def stop_blackjack(message: Message):
    # Получение данных о текущей игре
    player_hand = ctx.get("player_hand")
    player_score = ctx.get("player_score")
    dealer_hand = ctx.get("dealer_hand")
    dealer_score = ctx.get("dealer_score")

    # Дилер раздает карты себе, пока не достигнет 17 очков или выше
    while dealer_score < 17:
        card_info = await get_card(hand=player_hand + dealer_hand)
        dealer_hand.append(card_info[0])
        dealer_score += card_info[1]

    await message.answer(
        f"🙋‍♂Ваши карты:\n"
        f"{', '.join(player_hand)}\n"
        f"Счет: {player_score}\n\n"
        f"🤵Карты Крупье:\n"
        f"{', '.join(dealer_hand)}\n"
        f"Счет: {dealer_score}"
    )

    # Подведение итогов игры
    if dealer_score > 21 or player_score > dealer_score:
        await db.request(f"UPDATE users SET balance = balance + {ctx.get('bet')} * 2 WHERE vk_id = {message.from_id}")
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(
            '🙆‍♂️Поздравляю! Победа!\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    elif dealer_score == player_score:
        await db.request(f"UPDATE users SET balance = balance + {ctx.get('bet')} WHERE vk_id = {message.from_id}")
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(
            '💁‍♂️Пуш! Ничья\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    else:
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(
            '🤦‍♂️К сожалению, вы проиграли\nВозвращаю вас к списку игр',
            keyboard=games_menu_keyboard
        )
    ctx.storage.clear()


# Игра камень, ножницы, бумага
@bp.on.private_message(payload={'games': 'tsuefa'})
async def start_tsuefa(message: Message):
    await bp.state_dispenser.set(message.peer_id, Tsuefa.START)
    await message.answer(f"Камень, ножницы, бумага. Цу-е-фа!", keyboard=games_kb.tsuefa_keyboard)


@bp.on.message(state=Tsuefa.START)
async def tsuefa_game(message: Message):
    if message.payload:
        player_sign = json.loads(message.payload)['tsuefa']
        bot_sign = {1: "Камень", 2: "Ножницы", 3: "Бумага"}[random.randint(1, 3)]
        if player_sign == "Камень":
            if bot_sign == "Камень":
                await message.answer(f"👊Камень! Ничья 😏", keyboard=games_menu_keyboard)
            elif bot_sign == "Ножницы":
                await message.answer(f"✌Ножницы! Вы выиграли 😉", keyboard=games_menu_keyboard)
            elif bot_sign == "Бумага":
                await message.answer(f"✋Бумага! Вы проиграли 😕", keyboard=games_menu_keyboard)
        elif player_sign == "Ножницы":
            if bot_sign == "Камень":
                await message.answer(f"👊Камень! Вы проиграли 😕", keyboard=games_menu_keyboard)
            elif bot_sign == "Ножницы":
                await message.answer(f"✌Ножницы! Ничья 😏", keyboard=games_menu_keyboard)
            elif bot_sign == "Бумага":
                await message.answer(f"✋Бумага! Вы выиграли 😉", keyboard=games_menu_keyboard)
        elif player_sign == "Бумага":
            if bot_sign == "Камень":
                await message.answer(f"👊Камень! Вы выиграли 😉", keyboard=games_menu_keyboard)
            elif bot_sign == "Ножницы":
                await message.answer(f"✌Ножницы! Вы проиграли 😕", keyboard=games_menu_keyboard)
            elif bot_sign == "Бумага":
                await message.answer(f"✋Бумага! Ничья 😏", keyboard=games_menu_keyboard)
        elif player_sign == '◀ К списку игр':
            await message.answer(f'Список игр', keyboard=games_menu_keyboard)
        await bp.state_dispenser.delete(message.peer_id)
    else:
        await message.answer("❗ Некорректный ввод", keyboard=games_kb.tsuefa_keyboard)


# Игра монетка
@bp.on.private_message(payload={'games': 'coinflip'})
async def start_coin_flip(message: Message):
    await bp.state_dispenser.set(message.peer_id, CoinFlip.START)
    await message.answer(f"Игра «Монетка»", keyboard=games_kb.coin_flip_keyboard)


@bp.on.private_message(state=CoinFlip.START)
async def coin_flip_game(message: Message):
    if message.payload:
        answer = json.loads(message.payload)["coin_flip"]
        if message.payload == "back":
            await bp.state_dispenser.delete(message.peer_id)
            await message.answer(f'Список игр', keyboard=games_menu_keyboard)
        else:
            another_side = "Решка" if answer == "Орел" else "Орел"
            if random.randint(1, 2) == 1:
                await message.answer(f"🥳 {answer}! Вы выиграли!",  keyboard=games_menu_keyboard)
            else:
                await message.answer(f"😕 {another_side}! Вы проиграли", keyboard=games_menu_keyboard)
            await bp.state_dispenser.delete(message.peer_id)

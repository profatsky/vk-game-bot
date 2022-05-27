import datetime
import json
from typing import Union

from vkbottle import PhotoMessageUploader
from vkbottle.bot import Blueprint, Message

from loader import db
from keyboards import shop_kb
from keyboards.menu_kb import shop_menu_keyboard
from keyboards.income_kb import mining_keyboard
from image_app import create_shop_page
from blueprints.main_menu import profile, shop
import states

bp = Blueprint()


# Получение баланса
async def check_balance(user_id: int) -> int:
    balance = db.request(f"SELECT balance FROM users WHERE vk_id = {user_id}")['balance']
    return balance


# Раздел магазина для изменения внешнего вида для персонажа
@bp.on.private_message(payload={'shop_menu': 'customize'})
async def customize_menu(message: Message):
    await message.answer(
        "✨ Здесь вы можете изменить внешность вашего персонажа",
        keyboard=shop_kb.customize_keyboard
    )


async def show_customize_page(message: Message, kb, attribute: str, prices: tuple, nums: tuple = (1, 2, 3)):
    attributes = db.request(f"SELECT skin, face, haircut, clothes FROM users WHERE vk_id = {message.from_id}")
    img = await create_shop_page(
        user_attributes=attributes,
        attribute_type=attribute,
        prices=prices,
        nums=nums
    )
    photo = await PhotoMessageUploader(bp.api).upload(img)
    await bp.api.messages.send(
        peer_id=message.from_id,
        message='',
        keyboard=kb,
        attachment=photo,
        random_id=0)


# Приобретение предмета и списание средств
async def purchase(message: Message, attribute_type: str, attribute_value: Union[int, str], price: int):
    if await check_balance(message.from_id) > price:
        db.request(f'UPDATE users SET {attribute_type} = "{attribute_value}", balance = balance - {price} '
                   f'WHERE vk_id = {message.from_id}')
        await message.answer("🥳 Поздравляем с покупкой!")
        await bp.state_dispenser.delete(message.peer_id)
        await profile(message, kb=shop_menu_keyboard)
        return True
    await message.answer("😕 Недостаточно средств!")
    return False


# Создание изображения (первой страницы) с доступными цветами кожи
@bp.on.private_message(payload={"customize": "skin"})
async def show_skin_page_1(message: Message):
    await show_customize_page(
        message=message,
        attribute="skin",
        prices=(500, 500, 500),
        kb=shop_kb.choose_keyboard_shop_1
    )
    await bp.state_dispenser.set(message.peer_id, states.ChangeSkin.PAGE_1)


# Ответ на выбор пользователя при изменении цвета кожи на первой странице
@bp.on.private_message(state=states.ChangeSkin.PAGE_1)
async def select_skin_page_1(message: Message):
    if message.payload:
        choice = json.loads(message.payload)["choice"]
        exist_skin = db.request(f"SELECT skin FROM users WHERE vk_id = {message.from_id}")["skin"]
        if choice == "shop":
            await customize_menu(message)
        elif choice in (1, 2, 3) and choice != exist_skin:
            prices = {1: 500, 2: 500, 3: 500}
            await purchase(
                message=message,
                attribute_type="skin",
                attribute_value=choice,
                price=prices[choice]
            )
        else:
            await message.answer("❗ Вы выбрали уже имеющийся цвет кожи")
            await bp.state_dispenser.delete(message.peer_id)
            await profile(message)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=shop_kb.choose_keyboard_shop_1)


# Создание изображения (первой страницы) с доступными лицами
@bp.on.private_message(payload={"customize": "face"})
async def show_face_page_1(message: Message):
    await show_customize_page(
        message=message,
        attribute="face",
        prices=(500, 500, 500),
        kb=shop_kb.choose_keyboard_shop_2
    )
    await bp.state_dispenser.set(message.peer_id, states.ChangeFace.PAGE_1)


# Ответ на выбор пользователя при изменении лица на первой странице
@bp.on.private_message(state=states.ChangeFace.PAGE_1)
async def select_face_page_1(message: Message):
    if message.payload:
        choice = json.loads(message.payload)["choice"]
        exist_face = db.request(f"SELECT face FROM users WHERE vk_id = {message.from_id}")["face"]
        if choice == "shop":
            await bp.state_dispenser.delete(message.peer_id)
            await customize_menu(message)
        elif choice == "next":
            await show_face_page_2(message)
        elif choice in (1, 2, 3) and choice != exist_face:
            prices = {1: 500, 2: 500, 3: 500}
            await purchase(
                message=message,
                attribute_type="face",
                attribute_value=choice,
                price=prices[choice]
            )
        else:
            await message.answer("❗ Вы выбрали имеющееся лицо")
            await bp.state_dispenser.delete(message.peer_id)
            await profile(message)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=shop_kb.choose_keyboard_shop_2)


# Создание изображения (второй страницы) с доступными лицами
async def show_face_page_2(message: Message):
    await show_customize_page(
        message=message,
        attribute="face",
        prices=(1500, 2500, 5000),
        kb=shop_kb.choose_keyboard_shop_3,
        nums=(4, 5, 6)
    )
    await bp.state_dispenser.set(message.peer_id, states.ChangeFace.PAGE_2)


# Ответ на выбор пользователя при изменении лица на второй странице
@bp.on.private_message(state=states.ChangeFace.PAGE_2)
async def select_face_page_2(message: Message):
    if message.payload:
        choice = json.loads(message.payload)["choice"]
        exist_face = db.request(f"SELECT face FROM users WHERE vk_id = {message.from_id}")["face"]
        if choice == "shop":
            await bp.state_dispenser.delete(message.peer_id)
            await customize_menu(message)
        elif choice == "prev":
            await show_face_page_1(message)
        elif choice in (4, 5, 6) and choice != exist_face:
            prices = {4: 1500, 5: 2500, 6: 5000}  # id лица: цена
            await purchase(
                message=message,
                attribute_type="face",
                attribute_value=choice,
                price=prices[choice]
            )
        else:
            await message.answer("❗ Вы выбрали имеющееся лицо")
            await bp.state_dispenser.delete(message.peer_id)
            await profile(message)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=shop_kb.choose_keyboard_shop_3)


# Создание изображения (первой страницы) с доступными прическами
@bp.on.private_message(payload={"customize": "haircut"})
async def show_haircut_page_1(message: Message):
    await show_customize_page(
        message=message,
        attribute="haircut",
        prices=(500, 500, 500),
        kb=shop_kb.choose_keyboard_shop_2
    )
    await bp.state_dispenser.set(message.peer_id, states.ChangeHaircut.PAGE_1)


# Ответ на выбор пользователя при изменении прически на первой странице
@bp.on.private_message(state=states.ChangeHaircut.PAGE_1)
async def select_haircut_page_1(message: Message):
    if message.payload:
        choice = json.loads(message.payload)["choice"]
        exist_haircut = db.request(f"SELECT haircut FROM users WHERE vk_id = {message.from_id}")["haircut"]
        if choice == "shop":
            await bp.state_dispenser.delete(message.peer_id)
            await customize_menu(message)
        elif choice == "next":
            await show_haircut_page_2(message)
        elif choice in (1, 2, 3) and choice != exist_haircut:
            prices = {1: 500, 2: 500, 3: 500}
            result = await purchase(
                message=message,
                attribute_type="haircut",
                attribute_value=choice,
                price=prices[choice]
            )
            if result:
                await message.answer("🥳 Поздравляем с покупкой!")
                await bp.state_dispenser.delete(message.peer_id)
                await profile(message)
            else:
                await message.answer("😕 Недостаточно средств!")
        else:
            await message.answer("❗ Вы выбрали имеющуюся прическу")
            await bp.state_dispenser.delete(message.peer_id)
            await profile(message)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=shop_kb.choose_keyboard_shop_2)


# Создание изображения (второй страницы) с доступными прическами
async def show_haircut_page_2(message: Message):
    await show_customize_page(
        message=message,
        attribute="haircut",
        prices=(1500, 3000, 5000),
        kb=shop_kb.choose_keyboard_shop_4,
        nums=(4, 5, 6)
    )
    await bp.state_dispenser.set(message.peer_id, states.ChangeHaircut.PAGE_2)


# Ответ на выбор пользователя при изменении прически на второй странице
@bp.on.private_message(state=states.ChangeHaircut.PAGE_2)
async def select_haircut_page_2(message: Message):
    if message.payload:
        choice = json.loads(message.payload)["choice"]
        exist_haircut = db.request(f"SELECT haircut FROM users WHERE vk_id = {message.from_id}")["haircut"]
        if choice == "shop":
            await bp.state_dispenser.delete(message.peer_id)
            await customize_menu(message)
        elif choice == "prev":
            await show_haircut_page_1(message)
        elif choice == "next":
            await show_haircut_page_3(message)
        elif choice in (4, 5, 6) and choice != exist_haircut:
            prices = {4: 1500, 5: 3000, 6: 5000}
            await purchase(
                message=message,
                attribute_type="haircut",
                attribute_value=choice,
                price=prices[choice]
            )

        else:
            await message.answer("❗ Вы выбрали имеющуюся прическу")
            await bp.state_dispenser.delete(message.peer_id)
            await profile(message)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=shop_kb.choose_keyboard_shop_4)


# Создание изображения (третьей страницы) с доступными прическами
async def show_haircut_page_3(message: Message):
    await show_customize_page(
        message=message,
        attribute="haircut",
        prices=(10000, 15000, 30000),
        kb=shop_kb.choose_keyboard_shop_5,
        nums=(7, 8, 9)
    )
    await bp.state_dispenser.set(message.peer_id, states.ChangeHaircut.PAGE_3)


# Ответ на выбор пользователя при изменении прически на третьей странице
@bp.on.private_message(state=states.ChangeHaircut.PAGE_3)
async def select_haircut_page_3(message: Message):
    if message.payload:
        choice = json.loads(message.payload)["choice"]
        exist_haircut = db.request(f"SELECT haircut FROM users WHERE vk_id = {message.from_id}")["haircut"]
        if choice == "shop":
            await bp.state_dispenser.delete(message.peer_id)
            await customize_menu(message)
        elif choice == "prev":
            await show_haircut_page_2(message)
        elif choice in (7, 8, 9) and choice != exist_haircut:
            prices = {7: 10000, 8: 15000, 9: 30000}
            await purchase(
                message=message,
                attribute_type="haircut",
                attribute_value=choice,
                price=prices[choice]
            )
        else:
            await message.answer("❗ Вы выбрали имеющуюся прическу")
            await bp.state_dispenser.delete(message.peer_id)
            await profile(message)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=shop_kb.choose_keyboard_shop_5)


# Создание изображения (первой страницы) с доступной одеждой
@bp.on.private_message(payload={"customize": "clothes"})
async def show_clothes_page_1(message: Message):
    await show_customize_page(
        message=message,
        attribute="clothes",
        prices=(1000, 1000, 1000),
        kb=shop_kb.choose_keyboard_shop_1
    )
    await bp.state_dispenser.set(message.peer_id, states.ChangeClothes.PAGE_1)


# Ответ на выбор пользователя при изменении одежды на первой странице
@bp.on.private_message(state=states.ChangeClothes.PAGE_1)
async def select_clothes_page_1(message: Message):
    if message.payload:
        choice = json.loads(message.payload)["choice"]
        exist_clothes = db.request(f"SELECT clothes FROM users WHERE vk_id = {message.from_id}")["clothes"]
        if choice == "shop":
            await bp.state_dispenser.delete(message.peer_id)
            await customize_menu(message)
        elif choice in (1, 2, 3) and choice != exist_clothes:
            prices = {1: 1000, 2: 1000, 3: 1000}
            await purchase(
                message=message,
                attribute_type="clothes",
                attribute_value=choice,
                price=prices[choice]
            )
        else:
            await message.answer("❗ Вы выбрали имеющуюся одежду")
            await bp.state_dispenser.delete(message.peer_id)
            await profile(message)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=shop_kb.choose_keyboard_shop_1)


# Раздел магазина с видеокартами
@bp.on.private_message(payload={'mining_menu': 'buy_cards'})
async def mining_shop(message: Message):
    photo = await PhotoMessageUploader(bp.api).upload("files/images/video_cards/cards.png")
    await bp.api.messages.send(
        peer_id=message.from_id,
        message='📼 Видеокарты доступные для покупки\n\n❗ Каждый пользователь может владеть лишь 3 видеокартами',
        keyboard=shop_kb.buy_graphics_card_keyboard,
        attachment=photo,
        random_id=0
    )

    await bp.state_dispenser.set(message.peer_id, states.BuyCard.BUY)


# Добавление/изменение данных пользователя в таблицах при покупке видеокарты
async def add_mining(vk_id, video_card):
    if not db.request(f"SELECT * FROM mining JOIN users USING (user_id) WHERE vk_id = {vk_id}", "result"):
        db.request(f'INSERT INTO mining (user_id, {video_card}) '
                   f'VALUES ((SELECT user_id FROM users WHERE vk_id = {vk_id}), "{datetime.datetime.now()}")')
    else:
        db.request(f'UPDATE mining SET {video_card} = "{datetime.datetime.now()}" '
                   f'WHERE user_id = (SELECT user_id FROM users WHERE vk_id = {vk_id})')


# Ответ на выбор пользователя при покупке видеокарты
@bp.on.private_message(state=states.BuyCard.BUY)
async def buy_card(message: Message):
    if message.payload:
        choice = json.loads(message.payload)["choice"]
        if choice == "shop":
            await bp.state_dispenser.delete(message.peer_id)
            await shop(message)
        else:
            slots = db.request(f"SELECT slot_1, slot_2, slot_3 FROM users WHERE vk_id = {message.from_id}")
            # Проверяем, есть ли свободный слот у пользователя
            if "no_card" not in (slots["slot_1"], slots["slot_2"], slots["slot_3"]):
                await bp.state_dispenser.delete(message.peer_id)
                await message.answer(
                    '❗ Вы уже владеете максимальным количеством видеокарт',
                    keyboard=mining_keyboard
                )
            else:
                # Узнаем какой слот (одна из трех колонок в таблице) у пользователя свободен
                if slots['slot_1'] == "no_card":
                    free_slot = 'slot_1'
                elif slots['slot_2'] == "no_card":
                    free_slot = 'slot_2'
                else:
                    free_slot = 'slot_3'

                # Покупка видеокарты и сохранение ее названия в свободном слоте
                result = await purchase(
                    message=message,
                    attribute_type=free_slot,
                    attribute_value=choice[0],
                    price=choice[1]
                )
                if result:
                    await add_mining(vk_id=message.from_id, video_card=choice[0])
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=shop_kb.buy_graphics_card_keyboard)

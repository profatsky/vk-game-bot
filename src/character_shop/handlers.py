import dataclasses

from tortoise.expressions import Q, F
from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler
from vkbottle.modules import json

from character_shop.images import create_shop_image
from character_shop.keyboards import character_shop_keyboard
from character_shop.states import CharacterShopState
from config import bot
from images import upload_image, convert_image_to_bytes_io
from menu.handlers import show_profile
from menu.utils import generate_shop_keyboard
from users.models import UserModel, ClothesModel, FaceModel, SkinModel, HaircutModel
from users.utils import is_enough_money

bl = BotLabeler()


@bl.private_message(payload={'shop_menu': 'character'})
async def show_character_shop_menu(message: Message):
    await message.answer(
        "✨ Здесь вы можете изменить внешность вашего персонажа",
        keyboard=character_shop_keyboard
    )


@bl.private_message(payload={'character_shop': 'skin'})
async def show_skin_shop_page(message: Message, page_number: int = 1):
    user = await UserModel.get(vk_id=message.from_id)
    user = await user.convert_to_dataclass()

    skins = await SkinModel.filter(
        Q(pk__gte=page_number * 3 - 2) & Q(pk__lte=page_number * 3 + 1)
    )
    characters = []
    prices = []
    choice_numbers = []
    for skin in skins[:3]:
        character = dataclasses.replace(user.character)
        character.skin = skin.convert_to_dataclass()
        characters.append(character)
        prices.append(skin.price)
        choice_numbers.append(skin.pk)

    image = create_shop_image(characters, choice_numbers, prices)
    image = await upload_image(convert_image_to_bytes_io(image))

    keyboard = generate_shop_keyboard(
        numbers=choice_numbers,
        prev_page=(page_number > 1),
        next_page=(len(skins) == 4),
        back_label='◀🏬 В магазин'
    )

    await message.answer(
        message='',
        attachment=image,
        keyboard=keyboard
    )
    await bot.state_dispenser.set(
        message.from_id,
        CharacterShopState.CHANGE_SKIN,
        current_skin_pk=user.character.skin.pk,
        current_shop_page=page_number,
        keyboard=keyboard
    )


@bl.private_message(state=CharacterShopState.CHANGE_SKIN)
async def change_skin(message: Message):
    state_payload = message.state_peer.payload
    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=state_payload['keyboard']
        )

    choice = json.loads(message.payload)['choice']
    if choice == 'back':
        await bot.state_dispenser.delete(message.from_id)
        await show_character_shop_menu(message)
    elif choice == 'prev_page':
        await show_skin_shop_page(message, state_payload['current_shop_page'] - 1)
    elif choice == 'next_page':
        await show_skin_shop_page(message, state_payload['current_shop_page'] + 1)
    elif choice == state_payload['current_skin_pk']:
        await message.answer("❗ Вы выбрали уже имеющийся цвет кожи!")
        await bot.state_dispenser.delete(message.peer_id)
        await show_profile(message)
    else:
        chosen_skin = await SkinModel.get(pk=choice)
        if await is_enough_money(message.from_id, chosen_skin.price):
            await UserModel.filter(vk_id=message.from_id).update(
                skin_id=choice, balance=F('balance') - chosen_skin.price
            )
            await message.answer(f'🎨 Вы изменили цвет кожи за ${chosen_skin.price}')
            await bot.state_dispenser.delete(message.peer_id)
            await show_profile(message)
        else:
            await message.answer('❗ У вас недостаточно средств!')


@bl.private_message(payload={'character_shop': 'face'})
async def show_face_shop_page(message: Message, page_number: int = 1):
    user = await UserModel.get(vk_id=message.from_id)
    user = await user.convert_to_dataclass()

    faces = await FaceModel.filter(
        Q(pk__gte=page_number * 3 - 2) & Q(pk__lte=page_number * 3 + 1)
    )
    characters = []
    prices = []
    choice_numbers = []
    for face in faces[:3]:
        character = dataclasses.replace(user.character)
        character.face = face.convert_to_dataclass()
        characters.append(character)
        prices.append(face.price)
        choice_numbers.append(face.pk)

    image = create_shop_image(characters, choice_numbers, prices)
    image = await upload_image(convert_image_to_bytes_io(image))

    keyboard = generate_shop_keyboard(
        numbers=choice_numbers,
        prev_page=(page_number > 1),
        next_page=(len(faces) == 4),
        back_label='◀🏬 В магазин'
    )

    await message.answer(
        message='',
        attachment=image,
        keyboard=keyboard
    )
    await bot.state_dispenser.set(
        message.from_id,
        CharacterShopState.CHANGE_FACE,
        current_skin_pk=user.character.face.pk,
        current_shop_page=page_number,
        keyboard=keyboard
    )


@bl.private_message(state=CharacterShopState.CHANGE_FACE)
async def change_face(message: Message):
    state_payload = message.state_peer.payload
    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=state_payload['keyboard']
        )

    choice = json.loads(message.payload)['choice']
    if choice == 'back':
        await bot.state_dispenser.delete(message.from_id)
        await show_character_shop_menu(message)
    elif choice == 'prev_page':
        await show_face_shop_page(message, state_payload['current_shop_page'] - 1)
    elif choice == 'next_page':
        await show_face_shop_page(message, state_payload['current_shop_page'] + 1)
    elif choice == state_payload['current_skin_pk']:
        await message.answer("❗ Вы выбрали уже имеющееся лицо!")
        await bot.state_dispenser.delete(message.peer_id)
        await show_profile(message)
    else:
        chosen_face = await FaceModel.get(pk=choice)
        if await is_enough_money(message.from_id, chosen_face.price):
            await UserModel.filter(vk_id=message.from_id).update(
                face_id=choice, balance=F('balance') - chosen_face.price
            )
            await message.answer(f'🎭 Вы изменили лицо за ${chosen_face.price}')
            await bot.state_dispenser.delete(message.peer_id)
            await show_profile(message)
        else:
            await message.answer('❗ У вас недостаточно средств!')


@bl.private_message(payload={'character_shop': 'haircut'})
async def show_haircut_shop_page(message: Message, page_number: int = 1):
    user = await UserModel.get(vk_id=message.from_id)
    user = await user.convert_to_dataclass()

    haircuts = await HaircutModel.filter(
        Q(pk__gte=page_number * 3 - 2) & Q(pk__lte=page_number * 3 + 1)
    )
    characters = []
    prices = []
    choice_numbers = []
    for haircut in haircuts[:3]:
        character = dataclasses.replace(user.character)
        character.haircut = haircut.convert_to_dataclass()
        characters.append(character)
        prices.append(haircut.price)
        choice_numbers.append(haircut.pk)

    image = create_shop_image(characters, choice_numbers, prices)
    image = await upload_image(convert_image_to_bytes_io(image))

    keyboard = generate_shop_keyboard(
        numbers=choice_numbers,
        prev_page=(page_number > 1),
        next_page=(len(haircuts) == 4),
        back_label='◀🏬 В магазин'
    )

    await message.answer(
        message='',
        attachment=image,
        keyboard=keyboard
    )
    await bot.state_dispenser.set(
        message.from_id,
        CharacterShopState.CHANGE_HAIRCUT,
        current_haircut_pk=user.character.haircut.pk,
        current_shop_page=page_number,
        keyboard=keyboard
    )


@bl.private_message(state=CharacterShopState.CHANGE_HAIRCUT)
async def change_haircut(message: Message):
    state_payload = message.state_peer.payload
    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=state_payload['keyboard']
        )

    choice = json.loads(message.payload)['choice']
    if choice == 'back':
        await bot.state_dispenser.delete(message.from_id)
        await show_character_shop_menu(message)
    elif choice == 'prev_page':
        await show_haircut_shop_page(message, state_payload['current_shop_page'] - 1)
    elif choice == 'next_page':
        await show_haircut_shop_page(message, state_payload['current_shop_page'] + 1)
    elif choice == state_payload['current_haircut_pk']:
        await message.answer("❗ Вы выбрали уже имеющуюся прическу!")
        await bot.state_dispenser.delete(message.peer_id)
        await show_profile(message)
    else:
        chosen_haircut = await HaircutModel.get(pk=choice)
        if await is_enough_money(message.from_id, chosen_haircut.price):
            await UserModel.filter(vk_id=message.from_id).update(
                haircut_id=choice, balance=F('balance') - chosen_haircut.price
            )
            await message.answer(f'✂ Вы изменили прическу за ${chosen_haircut.price}')
            await bot.state_dispenser.delete(message.peer_id)
            await show_profile(message)
        else:
            await message.answer('❗ У вас недостаточно средств!')


@bl.private_message(payload={'character_shop': 'clothes'})
async def show_clothes_shop_page(message: Message, page_number: int = 1):
    user = await UserModel.get(vk_id=message.from_id)
    user = await user.convert_to_dataclass()

    clothes = await ClothesModel.filter(
        Q(pk__gte=page_number * 3 - 2) & Q(pk__lte=page_number * 3 + 1)
    )
    characters = []
    prices = []
    choice_numbers = []
    for item in clothes[:3]:
        character = dataclasses.replace(user.character)
        character.clothes = item.convert_to_dataclass()
        characters.append(character)
        prices.append(item.price)
        choice_numbers.append(item.pk)

    image = create_shop_image(characters, choice_numbers, prices)
    image = await upload_image(convert_image_to_bytes_io(image))

    keyboard = generate_shop_keyboard(
        numbers=choice_numbers,
        prev_page=(page_number > 1),
        next_page=(len(clothes) == 4),
        back_label='◀🏬 В магазин'
    )

    await message.answer(
        message='',
        attachment=image,
        keyboard=keyboard
    )
    clothes = user.character.clothes
    if clothes:
        clothes = clothes.pk
    await bot.state_dispenser.set(
        message.from_id,
        CharacterShopState.CHANGE_CLOTHES,
        current_clothes_pk=clothes,
        current_shop_page=page_number,
        keyboard=keyboard
    )


@bl.private_message(state=CharacterShopState.CHANGE_CLOTHES)
async def change_clothes(message: Message):
    state_payload = message.state_peer.payload
    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=state_payload['keyboard']
        )

    choice = json.loads(message.payload)['choice']
    if choice == 'back':
        await bot.state_dispenser.delete(message.from_id)
        await show_character_shop_menu(message)
    elif choice == 'prev_page':
        await show_clothes_shop_page(message, state_payload['current_shop_page'] - 1)
    elif choice == 'next_page':
        await show_clothes_shop_page(message, state_payload['current_shop_page'] + 1)
    elif choice == state_payload['current_clothes_pk']:
        await message.answer("❗ Вы выбрали уже имеющуюся одежду!")
        await bot.state_dispenser.delete(message.peer_id)
        await show_profile(message)
    else:
        chosen_clothes = await ClothesModel.get(pk=choice)
        if await is_enough_money(message.from_id, chosen_clothes.price):
            await UserModel.filter(vk_id=message.from_id).update(
                clothes_id=choice, balance=F('balance') - chosen_clothes.price
            )
            await message.answer(f'👕 Вы купили одежду за ${chosen_clothes.price}')
            await bot.state_dispenser.delete(message.peer_id)
            await show_profile(message)
        else:
            await message.answer('❗ У вас недостаточно средств!')

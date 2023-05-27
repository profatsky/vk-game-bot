from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler
from vkbottle.modules import json

from config import bot, ADMIN_ID, admin_list
from images import upload_image, convert_image_to_bytes_io
from menu.handlers import show_profile
from menu.keyboards import main_menu_keyboard
from menu.utils import get_main_menu_keyboard
from .images import create_choice_image
from .utils import is_user_exists
from .keyboards import register_choice_keyboard
from .models import UserModel, SkinModel, FaceModel, HaircutModel
from .models_representations import Character
from .states import RegisterState

bl = BotLabeler()


@bl.private_message(text='Начать')
async def start(message: Message):
    if await is_user_exists(message.from_id):
        await message.answer(
            '😕 Я вас не понимаю',
            keyboard=get_main_menu_keyboard(message.from_id)
        )
    else:
        image = await upload_image('assets/img/start.png')
        await message.answer(
            message='Выберите цвет кожи',
            attachment=image,
            keyboard=register_choice_keyboard
        )
        await bot.state_dispenser.set(message.from_id, RegisterState.CHOOSE_SKIN_COLOR)


@bl.private_message(state=RegisterState.CHOOSE_SKIN_COLOR)
async def choose_skin_color(message: Message):
    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=register_choice_keyboard
        )
    skin_choice = json.loads(message.payload)['choice']
    skin = await SkinModel.get(pk=skin_choice)
    skin_dataclass = skin.convert_to_dataclass()

    faces = await FaceModel.filter(pk__lte=3)
    faces_dataclasses = [face.convert_to_dataclass() for face in faces]

    characters = []
    for i in range(3):
        characters.append(
            Character(
                skin=skin_dataclass,
                face=faces_dataclasses[i]
            )
        )

    image = create_choice_image(
        characters=characters,
        choice_numbers=[1, 2, 3]
    )
    image = await upload_image(convert_image_to_bytes_io(image))
    await message.answer(
        message='Выберите лицо',
        attachment=image,
        keyboard=register_choice_keyboard
    )
    await bot.state_dispenser.set(
        message.from_id,
        RegisterState.CHOOSE_FACE,
        skin_dataclass=skin_dataclass
    )


@bl.private_message(state=RegisterState.CHOOSE_FACE)
async def choose_face(message: Message):
    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=register_choice_keyboard
        )
    skin_dataclass = message.state_peer.payload['skin_dataclass']

    face_choice = json.loads(message.payload)['choice']
    face = await FaceModel.get(pk=face_choice)
    face_dataclass = face.convert_to_dataclass()

    haircuts = await HaircutModel.filter(pk__lte=3)
    haircuts_dataclasses = [haircut.convert_to_dataclass() for haircut in haircuts]

    characters = []
    for i in range(3):
        characters.append(
            Character(
                skin=skin_dataclass,
                face=face_dataclass,
                haircut=haircuts_dataclasses[i]
            )
        )

    image = create_choice_image(
        characters=characters,
        choice_numbers=[1, 2, 3]
    )
    image = await upload_image(convert_image_to_bytes_io(image))
    await message.answer(
        message='Выберите прическу',
        attachment=image,
        keyboard=register_choice_keyboard
    )
    await bot.state_dispenser.set(
        message.from_id,
        RegisterState.CHOOSE_HAIRCUT,
        skin_dataclass=skin_dataclass,
        face_dataclass=face_dataclass
    )


@bl.private_message(state=RegisterState.CHOOSE_HAIRCUT)
async def choose_haircut(message: Message):
    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=register_choice_keyboard
        )
    state_payload = message.state_peer.payload
    skin_dataclass = state_payload['skin_dataclass']
    face_dataclass = state_payload['face_dataclass']

    haircut_choice = json.loads(message.payload)['choice']
    haircut = await FaceModel.get(pk=haircut_choice)
    haircut_dataclass = haircut.convert_to_dataclass()

    await message.answer('Как к вам обращаться? Напишите своё имя')
    await bot.state_dispenser.set(
        message.from_id,
        RegisterState.ENTER_NICKNAME,
        skin_pk=skin_dataclass.pk,
        face_pk=face_dataclass.pk,
        haircut_pk=haircut_dataclass.pk
    )


@bl.private_message(state=RegisterState.ENTER_NICKNAME, text='<nickname>')
async def choose_nickname(message: Message, nickname: str):
    if len(nickname) > 16:
        return await message.answer('❗ Длина имени не может превышать 16 символов')
    state_payload = message.state_peer.payload
    user = await UserModel.create(
        vk_id=message.from_id,
        nickname=nickname,
        skin_id=state_payload['skin_pk'],
        face_id=state_payload['face_pk'],
        haircut_id=state_payload['haircut_pk'],
        background_color_id=1
    )

    if message.from_id == int(ADMIN_ID):
        user.status = 'Основатель'
        await user.save(update_fields=['status'])
        admin_list.set(user.vk_id, user.status)

    await bot.state_dispenser.delete(message.from_id)
    await message.answer('🥳 Вы успешно зарегистрировались!')
    await show_profile(message)

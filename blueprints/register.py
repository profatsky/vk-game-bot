import json

from vkbottle.bot import Blueprint, Message
from vkbottle import PhotoMessageUploader

from loader import db, ctx
from keyboards import menu_kb
from image_app import create_face, create_haircut
from blueprints.main_menu import profile
import states

bp = Blueprint()


# Запуск бота (регистрация и создание персонажа)
@bp.on.private_message(text=["Начать"])
async def start(message: Message):
    if not (await db.request(f"SELECT * FROM users WHERE vk_id = '{message.from_id}'", "result")):
        photo = await PhotoMessageUploader(bp.api).upload('files/images/start.png')

        await bp.api.messages.send(
            peer_id=message.from_id,
            message='Выберите цвет кожи',
            keyboard=menu_kb.register_keyboard,
            attachment=photo,
            random_id=0)

        await bp.state_dispenser.set(message.peer_id, states.RegisterState.SKIN)
    else:
        await message.answer("Я вас не понимаю 🤨", keyboard=menu_kb.main_menu_keyboard)


# Выбор цвета кожи при создании персонажа
@bp.on.private_message(state=states.RegisterState.SKIN)
async def choose_skin(message: Message):
    if message.payload:
        answer = json.loads(message.payload)["choice"]
        ctx.set("skin", answer)

        photo = await PhotoMessageUploader(bp.api).upload(await create_face(answer))

        await bp.api.messages.send(
            peer_id=message.from_id,
            message='Выберите лицо',
            keyboard=menu_kb.register_keyboard,
            attachment=photo,
            random_id=0)

        await bp.state_dispenser.set(message.peer_id, states.RegisterState.FACE)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=menu_kb.register_keyboard)


# Выбор лица при создании персонажа
@bp.on.private_message(state=states.RegisterState.FACE)
async def choose_face(message: Message):
    if message.payload:
        answer = json.loads(message.payload)["choice"]
        ctx.set("face", answer)

        photo = await PhotoMessageUploader(bp.api).upload(await create_haircut(skin=ctx.get("skin"), face=answer))

        await bp.api.messages.send(
            peer_id=message.from_id,
            message='Выберите прическу',
            keyboard=menu_kb.register_keyboard,
            attachment=photo,
            random_id=0)

        await bp.state_dispenser.set(message.peer_id, states.RegisterState.HAIRCUT)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=menu_kb.register_keyboard)


# Выбор прически при создании персонажа
@bp.on.private_message(state=states.RegisterState.HAIRCUT)
async def choose_haircut(message: Message):
    if message.payload:
        answer = json.loads(message.payload)["choice"]
        ctx.set("haircut", answer)

        await message.answer('Как к вам обращаться? Напишите своё имя')
        await bp.state_dispenser.set(message.peer_id, states.RegisterState.NICKNAME)
    else:
        await message.answer(message="❗ Некорректный ввод", keyboard=menu_kb.register_keyboard)


# Выбор никнейма при создании персонажа
@bp.on.private_message(state=states.RegisterState.NICKNAME, text='<nickname>')
async def choose_nickname(message: Message, nickname=None):
    if len(nickname) > 16:
        await message.answer('❗ Имя не должно превышать 16 символов')
    else:
        await db.request(
            'INSERT INTO users (vk_id, skin, face, haircut, nickname) '
            f'VALUES ({message.from_id}, {ctx.get("skin")}, {ctx.get("face")}, {ctx.get("haircut")}, "{nickname}")'
        )
        ctx.storage.clear()

        await bp.state_dispenser.delete(message.peer_id)
        await profile(message)

from vkbottle.bot import Blueprint, Message

from loader import db
from keyboards import menu_kb
from states import Support

bp = Blueprint()


# Обращение в техподдержку
@bp.on.private_message(payload={'main_menu': 'help'})
async def need_help(message: Message):
    await message.answer(
        f"✏ Напишите свой вопрос или используйте кнопку, чтобы вернуться в главное меню",
        keyboard=menu_kb.back_keyboard
    )
    await bp.state_dispenser.set(message.peer_id, Support.ASK)


@bp.on.private_message(state=Support.ASK, text='<report>')
async def send_report(message: Message, report=None):
    if report == '◀ В главное меню':
        await bp.state_dispenser.delete(message.peer_id)
        await message.answer(f'Главное меню', keyboard=menu_kb.main_menu_keyboard)
    else:
        # Проверка, есть ли уже отправленное обращение без ответа от этого пользователя
        if not db.request(
                request=f"SELECT * FROM reports WHERE "
                        f"user_id = (SELECT user_id FROM users WHERE vk_id = {message.from_id}) and is_answered = '0'",
                types='result'
        ):
            if len(report) > 256:
                await message.answer(f"❗ Длина вашего вопроса не должна превышать 256 символов")
            else:
                db.request(
                    f"INSERT INTO reports (user_id, message) VALUES "
                    f"((SELECT user_id FROM users WHERE vk_id = {message.from_id}), '{report}')"
                )

                user = (await bp.api.users.get(user_id=message.from_id))[0]
                admins = db.request(f"SELECT vk_id FROM admins JOIN users USING (user_id)", 'fetchall')

                # Рассылка уведомления всем администраторам
                for admin in admins:
                    await bp.api.messages.send(
                        peer_id=admin['vk_id'],
                        message=f'❗ Пришло новое обращение от пользователя '
                                f'[id{user.id}|{user.first_name} {user.last_name}]\n\n'
                                f'Список обращений - /answer',
                        random_id=0
                    )

                await bp.state_dispenser.delete(message.peer_id)
                await message.answer(
                    '😉 Ваше обращение отправлено в техподдержку',
                    keyboard=menu_kb.main_menu_keyboard
                )
        else:
            await bp.state_dispenser.delete(message.peer_id)
            await message.answer(
                "❗ Ожидайте ответа на заданный вами ранее вопрос",
                keyboard=menu_kb.main_menu_keyboard
            )

import json
from datetime import datetime

from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from config import admin_list, bot
from menu.models import QuestionModel
from menu.utils import generate_choice_keyboard_with_pagination
from users.models import UserModel
from .keyboards import admin_menu_keyboard, support_menu_keyboard, back_to_support_menu_keyboard
from .states import SupportState

bl = BotLabeler()


@bl.private_message(payload={'menu': 'admin'})
async def open_admin_menu(message: Message):
    await message.answer('🗝 Открываю админ панель', keyboard=admin_menu_keyboard)


@bl.private_message(payload={'admin': 'admin_list'})
async def show_admin_list(message: Message):
    text = '📑 Список администраторов\n\n'
    status_emoji = {'Хелпер': '🦺', 'Администратор': '👔', 'Гл.Администратор': '🎩', 'Основатель': '👑'}
    for vk_id, status in admin_list.storage.items():
        user = (await bot.api.users.get(user_id=vk_id))[0]
        text += f'{status_emoji[status]} {status} - [id{user.id}|{user.first_name} {user.last_name}]\n'
    await message.answer(text, keyboard=admin_menu_keyboard)


@bl.private_message(payload={'admin': 'support'})
async def show_support_menu(message: Message):
    await message.answer('☎ Открываю меню технической поддержки', keyboard=support_menu_keyboard)


@bl.private_message(payload={'support': 'unanswered'})
async def show_unanswered_questions(message: Message, questions: list = None, page_number: int = 0):
    text = f'📃 Список открытых обращений | Страница {page_number + 1}'

    if not questions:
        questions = await QuestionModel.filter(answer=None)
    number_of_questions = len(questions)

    questions_ids = []
    for q in questions[page_number * 3:page_number * 3 + 3]:
        questions_ids.append(q.pk)
        user = (await bot.api.users.get(user_id=(await q.from_user).vk_id))[0]
        text += f'\n\n№{q.pk}. {q.text}\nОтправитель: [id{user.id}|{user.first_name} {user.last_name}]'

    kb = generate_choice_keyboard_with_pagination(
        numbers=questions_ids,
        prev_page=(page_number > 0),
        next_page=True if number_of_questions - (page_number * 3 + 3) > 0 else False,
        back_label='◀⁉ Меню тех.поддержки'
    )
    await message.answer(text, keyboard=kb)
    await bot.state_dispenser.set(
        message.from_id,
        SupportState.SHOW_QUESTIONS,
        questions=questions,
        number_of_questions=number_of_questions,
        current_page=page_number,
        keyboard=kb
    )


@bl.private_message(state=SupportState.SHOW_QUESTIONS)
async def choose_question_to_answer(message: Message):
    state_payload = message.state_peer.payload
    if not message.payload:
        return await message.answer(
            message='❗ Некорректный ввод!',
            keyboard=state_payload['keyboard']
        )

    choice = json.loads(message.payload)['choice']
    if choice == 'back':
        await bot.state_dispenser.delete(message.from_id)
        await show_support_menu(message)
    elif choice == 'prev_page':
        await show_unanswered_questions(
            message,
            questions=state_payload['questions'],
            page_number=state_payload['current_page'] - 1
        )
    elif choice == 'next_page':
        await show_unanswered_questions(
            message,
            questions=state_payload['questions'],
            page_number=state_payload['current_page'] + 1
        )
    else:
        await bot.state_dispenser.set(
            message.from_id,
            SupportState.ANSWER_QUESTION,
            question_id=choice
        )
        await message.answer(
            f'📞 Для ответа выбран вопрос №{choice}\n\n'
            f'❗ Напишите ответ на вопрос или воспользуйтесь кнопкой, чтобы вернуться в меню тех.поддержки',
            keyboard=back_to_support_menu_keyboard
        )


@bl.private_message(state=SupportState.ANSWER_QUESTION, text='<text>')
async def answer_question(message: Message, text=None):
    if text == '◀☎ В меню тех.поддержки':
        await bot.state_dispenser.delete(message.from_id)
        await show_support_menu(message)
    elif len(text) > 512:
        await message.answer(
            '❗ Длина ответа не должна превышать 512 символов!',
            keyboard=back_to_support_menu_keyboard
        )
    else:
        question = await QuestionModel.get(pk=message.state_peer.payload['question_id'])
        question.answer = text
        question.answered_by = await UserModel.get(vk_id=message.from_id)
        question.answered_at = datetime.now()
        await question.save(update_fields=['answer', 'answered_by_id', 'answered_at'])
        await bot.state_dispenser.delete(message.from_id)
        await message.answer('✔ Ответ успешно отправлен!', keyboard=support_menu_keyboard)

        admin = (await bot.api.users.get(user_id=message.from_id))[0]
        await bot.api.messages.send(
            user_id=(await question.from_user).vk_id,
            random_id=0,
            message='✨ Пришел ответ от тех.поддержки на ваш вопрос!\n\n'
                    f'{text}\nОтправитель: [id{admin.id}|{admin.first_name} {admin.last_name}]'
        )

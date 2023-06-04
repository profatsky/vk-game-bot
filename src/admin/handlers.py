import json
import random
from datetime import datetime

from tortoise.exceptions import DoesNotExist
from vkbottle import Keyboard
from vkbottle.bot import Message
from vkbottle.framework.labeler import BotLabeler

from config import admin_list, bot, ADMIN_GRADES, USER_STATUSES
from menu.utils import generate_choice_keyboard_with_pagination
from users.handlers import start
from users.models import UserModel
from users.utils import get_clickable_user_name
from .models import QuestionModel
from .keyboards import admin_menu_keyboard, support_menu_keyboard, back_to_support_menu_keyboard, back_to_questions_list
from .states import UnansweredQuestionsState, AnsweredQuestionsState

bl = BotLabeler()


@bl.private_message(payload={'menu': 'admin'})
async def open_admin_menu(message: Message):
    await message.answer('🗝 Открываю админ панель', keyboard=admin_menu_keyboard)


@bl.private_message(payload={'admin': 'admin_list'})
async def show_admin_list(message: Message):
    text = '📑 Список администраторов\n\n'
    for vk_id, status in admin_list.storage.items():
        text += f'{ADMIN_GRADES[status]["emoji"]} {status} - {await get_clickable_user_name(vk_id)}\n'
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

    if not number_of_questions:
        return await message.answer(
            '😕 Список обращений пуст',
            keyboard=support_menu_keyboard
        )

    questions_ids = []
    for q in questions[page_number * 3:page_number * 3 + 3]:
        questions_ids.append(q.pk)
        text += f'\n\n🔹№{q.pk}' \
                f'💬 {q.text}\n' \
                f'👤 Отправитель: {await get_clickable_user_name((await q.from_user).vk_id)}'

    kb = generate_choice_keyboard_with_pagination(
        numbers=questions_ids,
        prev_page=(page_number > 0),
        next_page=True if number_of_questions - (page_number * 3 + 3) > 0 else False,
        back_label='◀⁉ Обращения'
    )
    await message.answer(text, keyboard=kb)
    await bot.state_dispenser.set(
        message.from_id,
        UnansweredQuestionsState.SHOW_UNANSWERED_QUESTIONS,
        questions=questions,
        number_of_questions=number_of_questions,
        current_page=page_number,
        keyboard=kb
    )


@bl.private_message(state=UnansweredQuestionsState.SHOW_UNANSWERED_QUESTIONS)
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
            UnansweredQuestionsState.ANSWER_QUESTION,
            question_id=choice
        )
        await message.answer(
            f'📞 Для ответа выбран вопрос №{choice}\n\n'
            f'❗ Напишите ответ на вопрос или воспользуйтесь кнопкой, чтобы вернуться в меню тех.поддержки',
            keyboard=back_to_support_menu_keyboard
        )


@bl.private_message(state=UnansweredQuestionsState.ANSWER_QUESTION, text='<text>')
async def answer_question(message: Message, text=None):
    if text == '◀☎ Обращения':
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

        await bot.api.messages.send(
            user_id=(await question.from_user).vk_id,
            random_id=random.randint(1, 2 ** 32),
            message='✨ Пришел ответ от тех.поддержки на ваш вопрос!\n\n'
                    f'💬 Текст ответа: {text}\n👔 Отправитель: {await get_clickable_user_name(message.from_id)}'
        )


@bl.private_message(payload={'support': 'answered'})
async def show_answered_questions(message: Message, questions: list = None, page_number: int = 0):
    text = f'📃 Список закрытых обращений | Страница {page_number + 1}'

    if not questions:
        questions = await QuestionModel.exclude(answer=None)
    number_of_questions = len(questions)

    if not number_of_questions:
        return await message.answer(
            '😕 Список обращений пуст',
            keyboard=support_menu_keyboard
        )

    questions_ids = []
    for q in questions[page_number * 3:page_number * 3 + 3]:
        questions_ids.append(q.pk)
        text += f'\n\n🔹 Обращение №{q.pk}\n' \
                f'💬 Текст обращения: {q.text}\n' \
                f'👤 Отправил: {await get_clickable_user_name((await q.from_user).vk_id)}\n' \
                f'👔 Ответил: {await get_clickable_user_name((await q.answered_by).vk_id)}'

    kb = generate_choice_keyboard_with_pagination(
        numbers=questions_ids,
        prev_page=(page_number > 0),
        next_page=True if number_of_questions - (page_number * 3 + 3) > 0 else False,
        back_label='◀⁉ Обращения'
    )
    await message.answer(text, keyboard=kb)
    await bot.state_dispenser.set(
        message.from_id,
        AnsweredQuestionsState.SHOW_ANSWERED_QUESTIONS,
        questions=questions,
        number_of_questions=number_of_questions,
        current_page=page_number,
        keyboard=kb
    )


@bl.private_message(state=AnsweredQuestionsState.SHOW_ANSWERED_QUESTIONS)
async def choose_question_to_get_info(message: Message):
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
    elif choice == 'current_page':
        await show_answered_questions(
            message,
            questions=state_payload['questions'],
            page_number=state_payload['current_page']
        )
    elif choice == 'prev_page':
        await show_answered_questions(
            message,
            questions=state_payload['questions'],
            page_number=state_payload['current_page'] - 1
        )
    elif choice == 'next_page':
        await show_answered_questions(
            message,
            questions=state_payload['questions'],
            page_number=state_payload['current_page'] + 1
        )
    else:
        question = await QuestionModel.get(pk=choice)

        await message.answer(
            f'📑 Детальная информация об обращении №{choice}\n\n'
            f'💬 Текст обращения: {question.text}\n'
            f'👤 Отправил: {await get_clickable_user_name((await question.from_user).vk_id)}\n'
            f'🕐 Время отправки: {question.created_at.strftime("%X %x")}\n\n'
            f'💬 Текст ответа: {question.answer}\n'
            f'👔 Ответил: {await get_clickable_user_name((await question.answered_by).vk_id)}\n'
            f'🕗 Время ответа: {question.answered_at.strftime("%X %x")}\n\n'
            '❗ Чтобы вернуться назад воспользуйтесь кнопкой',
            keyboard=back_to_questions_list
        )


@bl.private_message(payload={'support': 'answered_by_me'})
async def show_questions_answered_by_me(message: Message):
    questions = await QuestionModel.filter(
        answer__isnull=False,
        answered_by=await UserModel.get(
            vk_id=message.from_id
        )
    )
    await show_answered_questions(message, questions)


@bl.private_message(payload={'admin': 'stats'})
async def show_admin_stats(message: Message):
    user = await UserModel.get(vk_id=message.from_id)
    questions = await QuestionModel.filter(answered_by=user.pk).count()
    await message.answer(
        f'📉 Статистика {await get_clickable_user_name(message.from_id)}\n\n'
        f'{ADMIN_GRADES[user.status]["emoji"]} Админ-статус: {user.status}\n'
        f'☎ Кол-во ответов на обращения: {questions}\n',
        keyboard=admin_menu_keyboard
    )


@bl.private_message(payload={'admin': 'commands'})
async def show_admin_commands_list(message: Message):
    admin = await UserModel.get(vk_id=message.from_id)
    admin_lvl = ADMIN_GRADES[admin.status]['lvl']

    text = ''
    for grade in ADMIN_GRADES.values():
        if grade['lvl'] <= admin_lvl:
            for command in grade['commands']:
                text += f'\n{command}'

    await message.answer(
        f'🛠 Список доступных команд\n{text}' if text else '😕 Для вас нет доступных команд',
        keyboard=admin_menu_keyboard
    )


@bl.private_message(text='/setstatus <vk_id> <lvl>')
async def set_user_status(message: Message, vk_id: str = None, lvl: str = None):
    appointing_admin = await UserModel.get(vk_id=message.from_id)
    if appointing_admin.status == 'Пользователь':
        return await start(message)

    appointing_admin_lvl = ADMIN_GRADES[appointing_admin.status]['lvl']

    if not vk_id.isdigit() or not lvl.isdigit() or '0' in (vk_id, lvl):
        return await message.answer(
            '❗ Некорректный ввод! ID пользователя и уровень должны быть положительными числами!',
            keyboard=admin_menu_keyboard
        )
    vk_id, lvl = int(vk_id), int(lvl)

    if vk_id == message.from_id:
        return await message.answer(
            '❗ Некорректный ввод! Вы не можете изменить свой статус!',
            keyboard=admin_menu_keyboard
        )

    try:
        appointee = await UserModel.get(vk_id=vk_id)
    except DoesNotExist:
        return await message.answer('❗ Указанный пользователь не зарегистрирован!')
    appointee_lvl = ADMIN_GRADES.get(appointee.status)
    if appointee_lvl is None:
        appointee_lvl = 0

    if appointee_lvl >= appointing_admin_lvl or appointing_admin_lvl <= lvl:
        return await message.answer('❗ У вас недостаточно прав!', keyboard=admin_menu_keyboard)

    if appointee_lvl == lvl:
        return await message.answer(
            '❗ Пользователь уже имеет указанный статус!',
            keyboard=admin_menu_keyboard
        )

    appointee.status = USER_STATUSES[lvl]
    await appointee.save(update_fields=['status'])

    if lvl > 1:
        admin_list.set(vk_id, appointee.status)
    else:
        admin_list.delete(vk_id)

    await message.answer(
        f'✔ Вы изменили статус пользователя {await get_clickable_user_name(vk_id)} на «{appointee.status}»!',
        keyboard=admin_menu_keyboard
    )

    emoji = '⏫' if appointee_lvl < lvl else '⏬'
    await bot.api.messages.send(
        user_id=vk_id,
        random_id=random.randint(1, 2 ** 32),
        message=f'{emoji} {appointing_admin.status} {await get_clickable_user_name(message.from_id)} '
                f'изменил ваш статус на «{appointee.status}»!'
    )


@bl.private_message(text='/givemoney <vk_id> <money>')
async def give_money_to_user(message: Message, vk_id: str = None, money: str = None):
    admin = await UserModel.get(vk_id=message.from_id)

    if admin.status == 'Пользователь':
        return await start(message)

    if not vk_id.isdigit() or not money.isdigit() or '0' in (vk_id, money):
        return await message.answer(
            '❗ Некорректный ввод! ID пользователя и сумма должны быть положительными числами!',
            keyboard=admin_menu_keyboard
        )
    vk_id, money = int(vk_id), int(money)

    try:
        recipient = await UserModel.get(vk_id=vk_id)
    except DoesNotExist:
        return await message.answer('❗ Указанный пользователь не зарегистрирован!')

    if admin.status not in ('Гл.Администратор', 'Основатель'):
        return await message.answer(
            '❗ У вас недостаточно прав! Данной командой может воспользоваться только '
            'пользователь со статусом «Гл.Администратор» или «Основатель»!',
            keyboard=admin_menu_keyboard
        )

    recipient.balance += money
    await recipient.save(update_fields=['balance'])

    await message.answer(
        f'✔ Баланс пользователя {await get_clickable_user_name(recipient.vk_id)} успешно пополнен на ${money}!',
        keyboard=admin_menu_keyboard
    )

    await bot.api.messages.send(
        user_id=vk_id,
        random_id=random.randint(1, 2 ** 32),
        message=f'💸 {admin.status} {await get_clickable_user_name(message.from_id)} '
                f'пополнил ваш баланс на ${money}!'
    )


@bl.private_message(text='/setmoney <vk_id> <money>')
async def set_money_for_user(message: Message, vk_id: str = None, money: str = None):
    admin = await UserModel.get(vk_id=message.from_id)

    if admin.status == 'Пользователь':
        return await start(message)

    if not vk_id.isdigit() or not money.isdigit() or '0' in (vk_id, money):
        return await message.answer(
            '❗ Некорректный ввод! ID пользователя и сумма должны быть положительными числами!',
            keyboard=admin_menu_keyboard
        )
    vk_id, money = int(vk_id), int(money)

    try:
        recipient = await UserModel.get(vk_id=vk_id)
    except DoesNotExist:
        return await message.answer('❗ Указанный пользователь не зарегистрирован!')

    if admin.status not in ('Гл.Администратор', 'Основатель'):
        return await message.answer(
            '❗ У вас недостаточно прав! Данной командой может воспользоваться только '
            'пользователь со статусом «Гл.Администратор» или «Основатель»!',
            keyboard=admin_menu_keyboard
        )

    recipient.balance = money
    await recipient.save(update_fields=['balance'])

    await message.answer(
        f'✔ Баланс пользователя {await get_clickable_user_name(recipient.vk_id)} успешно изменен на ${money}!',
        keyboard=admin_menu_keyboard
    )

    await bot.api.messages.send(
        user_id=vk_id,
        random_id=random.randint(1, 2 ** 32),
        message=f'💵 {admin.status} {await get_clickable_user_name(message.from_id)} '
                f'изменил ваш баланс на ${money}!'
    )


@bl.private_message(text='/del <vk_id>')
async def del_user_account(message: Message, vk_id: str = None):
    admin = await UserModel.get(vk_id=message.from_id)

    if admin.status == 'Пользователь':
        return await start(message)

    if not vk_id.isdigit():
        return await message.answer(
            '❗ Некорректный введен ID пользователя!',
            keyboard=admin_menu_keyboard
        )
    vk_id = int(vk_id)

    try:
        user = await UserModel.get(vk_id=vk_id)
    except DoesNotExist:
        return await message.answer('❗ Указанный пользователь не зарегистрирован!')

    if admin.status != 'Основатель':
        return await message.answer(
            '❗ У вас недостаточно прав! Данной командой может воспользоваться только '
            'пользователь со статусом «Основатель»!',
            keyboard=admin_menu_keyboard
        )

    await user.delete()

    await message.answer(
        f'✔ Аккаунт пользователя {await get_clickable_user_name(user.vk_id)} удалён!',
        keyboard=admin_menu_keyboard
    )

    await bot.api.messages.send(
        user_id=vk_id,
        random_id=random.randint(1, 2 ** 32),
        message=f'❗❌ {admin.status} {await get_clickable_user_name(message.from_id)} удалил ваш аккаунт!',
        keyboard=Keyboard()
    )
    
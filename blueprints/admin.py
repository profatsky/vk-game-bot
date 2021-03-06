from vkbottle.bot import Blueprint, Message

from loader import db

bp = Blueprint()


# Проверка на принадлежность к касте администраторов
async def is_admin(vk_id: int) -> int:
    return db.request(
        f"SELECT lvl FROM admins WHERE user_id = (SELECT user_id FROM users WHERE vk_id = {vk_id})")['lvl']


# Проверка, зарегистрирован ли пользователь
async def is_registered(vk_id: int) -> int:
    return db.request(
        request=f"SELECT * FROM users WHERE vk_id = {vk_id}",
        types="result"
    )


# Узнать, занимает ли пользователь какую-либо должность
async def check_status(vk_id: int) -> str:
    lvl = db.request(f"SELECT lvl FROM admins WHERE user_id = (SELECT user_id FROM users WHERE vk_id = {vk_id})")
    statuses = {1: "Хелпер", 2: "Модератор", 3: "Администратор", 4: "Разработчик", 5: "Основатель"}
    if lvl:
        return statuses[lvl["lvl"]]
    else:
        return 'Пользователь'


# Проверка на наличие обращений в техподдержку
@bp.on.private_message(text="/reports")
async def check_reports(event: Message):
    reports = db.request(
        request="SELECT vk_id, message FROM reports JOIN users USING (user_id) WHERE is_answered = 0",
        types="fetchmany",
        size=3
    )
    if reports:
        # Формирование и демонастрация 3 обращений
        text = "📒 Список обращений\n\n"
        for count, report in enumerate(reports, start=1):
            user = (await bp.api.users.get(user_id=report['vk_id']))[0]
            text += f"{count}. Сообщение от пользователя [id{user.id}|{user.first_name} {user.last_name}]:\n" \
                    f"✉ {report['message']}\n❗ Для ответа - /answer {user.id}\n\n"
        await event.answer(f'{text}')
    else:
        await event.answer(f'❗ Обращений нет')


# Ответить на обращение пользователя
@bp.on.private_message(text='/answer <vk_id> <text>')
async def answer(message: Message, vk_id=None, text=None):
    if await is_admin(message.from_id):
        if vk_id and text:
            vk_id = int(vk_id)
            report_info = db.request(
                    request=f"SELECT * FROM reports WHERE user_id = (SELECT user_id FROM users WHERE vk_id = {vk_id}) "
                            f"and is_answered = 0"
            )
            if report_info:
                await bp.api.messages.send(
                    peer_id=vk_id,
                    message=f'❗ Пришел ответ от техподдержки!\n\n'
                            f'☎ Ваше обращение: {report_info["message"]}\n\n'
                            f'✉Ответ: {text}',
                    random_id=0
                )
                db.request(f"UPDATE reports SET is_answered = 1 WHERE vk_id = {vk_id} and is_answered = 0")
            else:
                await message.answer(f'❗ Нет обращений от указанного пользователя')
        else:
            await message.answer(f'❗ Используйте - /answer <id> <сообщение>')
    else:
        await message.answer(f"❗ У вас недостаточно прав")


@bp.on.private_message(text="/makeadmin <vk_id> <lvl>")
async def make_admin(message: Message, vk_id=None, lvl=None):
    if await is_admin(message.from_id):  # проверка, администратор ли отправил команду
        vk_id, lvl = int(vk_id), int(lvl)
        if await is_registered(vk_id):  # есть ли назначаемый пользователь в базе
            admin_lvl = db.request(
                f"SELECT lvl FROM admins WHERE user_id = (SELECT user_id FROM users WHERE vk_id = {message.from_id})"
            )['lvl']
            if admin_lvl < 3 or admin_lvl <= lvl:
                await message.answer(
                    "❗ Ваша должность должна быть выше должности, на которую вы хотите поставить пользователя"
                )
            else:
                candidate = (await bp.api.users.get(user_id=vk_id))[0]
                admin = (await bp.api.users.get(user_id=message.from_id))[0]
                admin_status = await check_status(message.from_id)

                candidate_lvl = await is_admin(vk_id)  # уровень администратора указанного пользователя
                if candidate_lvl:  # если указанный пользователь имеет права администратора
                    # Изменение уровня админ прав у указанного пользователя
                    db.request(
                        f"UPDATE admins SET lvl = {lvl} "
                        f"WHERE user_id = (SELECT user_id FROM users WHERE vk_id = {vk_id})"
                    )
                    candidate_status = await check_status(vk_id)
                    if candidate_lvl < lvl:  # повышение
                        # Отправка уведомления о повышении указанному пользователю
                        await bp.api.messages.send(
                            peer_id=vk_id,
                            message=f"🥳 {admin_status} [id{admin.id}|{admin.first_name} {admin.last_name}] "
                                    f"повысил вас до должности {candidate_status}а!",
                            random_id=0
                        )
                        # Ответ для администратора
                        await message.answer(
                            f"Вы повысили [id{candidate.id}|{candidate.first_name} {candidate.last_name}] "
                            f"до должности {candidate_status}а уровня!"
                        )

                    elif candidate_lvl > lvl:  # понижение
                        # Отправка уведомления о понижении указанному пользователю
                        await bp.api.messages.send(
                            peer_id=vk_id,
                            message=f"😕 Администратор [id{admin.id}|{admin.first_name} {admin.last_name}] "
                                    f"понизил вас до должности администратора {lvl} уровня",
                            random_id=0
                        )
                        # Ответ для администратора
                        await message.answer(
                            f"Вы понизили [id{candidate.id}|{candidate.first_name} {candidate.last_name}] "
                            f"до должности администратора {lvl} уровня"
                        )
                    else:
                        await message.answer(f"❗ Указанный пользователь и так имеет {lvl} уровень администратора")
                else:  # если указанный пользователь не имеет прав администратора
                    db.request(
                        f"INSERT INTO admins (user_id, lvl) "
                        f"VALUES ((SELECT user_id FROM users WHERE vk_id = {vk_id}), {lvl})"
                    )
                    candidate_status = await check_status(vk_id)
                    # Отправка уведомления о назначении на пост администратора указанному пользователю
                    await bp.api.messages.send(
                        peer_id=vk_id,
                        message=f"🥳 {admin_status} [id{admin.id}|{admin.first_name} {admin.last_name}] "
                                f"назначил вас на должность  {candidate_status}а!",
                        random_id=0
                    )
                    # Ответ для администратора
                    await message.answer(
                        f"Вы понизили [id{candidate.id}|{candidate.first_name} {candidate.last_name}] "
                        f"до должности {candidate_status}а!"
                    )
        else:
            await message.answer(f"❗ Указанного пользователя нет в базе")
    else:
        await message.answer(f"❗ У вас недостаточно прав")

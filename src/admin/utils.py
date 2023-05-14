from tortoise.expressions import Q

from config import admin_list
from users.models import UserModel


async def save_admin_list():
    for user in await UserModel.filter(~Q(status='Пользователь')):
        admin_list.set(user.vk_id, user.status)

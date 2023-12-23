from tortoise.exceptions import DoesNotExist
from tortoise.expressions import Q

from core.settings import ADMIN_ID
from core.loader import admin_list
from users.models import UserModel


async def appoint_superuser():
    try:
        superuser = await UserModel.get(vk_id=ADMIN_ID)
    except DoesNotExist:
        pass
    else:
        if superuser.status != 'Основатель':
            superuser.status = 'Основатель'
            await superuser.save(update_fields=['status'])


async def save_admin_list():
    for user in await UserModel.filter(~Q(status='Пользователь')):
        admin_list.set(user.vk_id, user.status)

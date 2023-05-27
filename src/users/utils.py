from vkbottle_types.codegen.objects import UsersUserFull

from config import bot
from .models import UserModel


async def is_user_exists(vk_id: int) -> bool:
    return await UserModel.exists(vk_id=vk_id)


async def is_enough_money(vk_id: int, money: int) -> bool:
    user_balance = await get_user_balance(vk_id)
    return user_balance >= money


async def get_user_balance(vk_id: int) -> int:
    user = await UserModel.get(vk_id=vk_id)
    return user.balance


async def get_free_gpu_slot(vk_id: int) -> str | None:
    user = await UserModel.get(vk_id=vk_id)
    if not user.gpu_1:
        return 'gpu_1'
    elif not user.gpu_2:
        return 'gpu_2'
    elif not user.gpu_3:
        return 'gpu_3'


async def get_clickable_user_name(vk_id: int) -> str:
    user_info = await get_user_info(vk_id)
    return f'[id{user_info.id}|{user_info.first_name} {user_info.last_name}]'


async def get_user_name(vk_id: int) -> str:
    user_info = await get_user_info(vk_id)
    return f'{user_info.first_name} {user_info.last_name}'


async def get_user_info(vk_id: int) -> UsersUserFull:
    return (await bot.api.users.get(user_ids=[vk_id]))[0]

from database.models import UserModel


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

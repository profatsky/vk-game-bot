from database.models import UserModel


async def is_user_exists(vk_id: int) -> bool:
    return await UserModel.exists(vk_id=vk_id)


async def is_enough_money(vk_id: int, money: int) -> bool:
    user_balance = await get_user_balance(vk_id)
    return user_balance >= money


async def get_user_balance(vk_id: int) -> int:
    user = await UserModel.get(vk_id=vk_id)
    return user.balance

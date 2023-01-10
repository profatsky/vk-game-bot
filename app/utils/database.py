from database.models import UserModel


async def is_user_exists(vk_id: int):
    return await UserModel.exists(vk_id=vk_id)

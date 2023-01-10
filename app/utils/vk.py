from io import BytesIO

from vkbottle import PhotoMessageUploader
from vkbottle_types.codegen.objects import UsersUserFull

from config import bot


async def upload_image(file_source: str | bytes | BytesIO) -> str | list[dict]:
    return await PhotoMessageUploader(bot.api).upload(file_source)


async def get_user_name(vk_id: int) -> str:
    user_info = await get_user_info(vk_id)
    return f"{user_info.first_name} {user_info.last_name}"


async def get_user_info(vk_id: int) -> UsersUserFull:
    return (await bot.api.users.get(user_ids=[vk_id]))[0]

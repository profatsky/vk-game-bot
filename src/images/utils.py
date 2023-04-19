from io import BytesIO

from vkbottle import PhotoMessageUploader

from config import bot


async def upload_image(file_source: str | bytes | BytesIO) -> str | list[dict]:
    return await PhotoMessageUploader(bot.api).upload(file_source)

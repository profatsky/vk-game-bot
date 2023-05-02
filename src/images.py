from io import BytesIO

from PIL import Image
from vkbottle import PhotoMessageUploader

from config import bot


def open_image(image_path: str):
    return Image.open(f'assets/img/{image_path}')


def convert_image_to_bytes_io(img: Image, image_path: str = 'img') -> BytesIO:
    bio = BytesIO()
    bio.name = image_path
    img.save(bio, 'png')
    bio.seek(0)
    return bio


async def upload_image(file_source: str | bytes | BytesIO) -> str | list[dict]:
    return await PhotoMessageUploader(bot.api).upload(file_source)

import asyncio
import os
from collections.abc import Callable
from io import BytesIO
from typing import Any

from PIL import Image

from core.loader import process_pool, photo_message_uploader
from core.settings import IMG_DIR


def open_image(image_path: str) -> Image:
    full_image_path = os.path.join(IMG_DIR, image_path)
    return Image.open(full_image_path)


def convert_image_to_bytes(img: Image, image_path: str = 'img') -> bytes:
    bio = BytesIO()
    bio.name = image_path
    img.save(bio, 'png')
    bio.seek(0)
    return bio.getvalue()


async def upload_image(file_source: str | bytes) -> str | list[dict]:
    return await photo_message_uploader.upload(file_source)


async def run_func_in_process(func: Callable, *args) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(process_pool, func, *args)

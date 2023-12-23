import asyncio
from collections.abc import Callable
from typing import Any

from config import process_pool


async def run_func_in_process(func: Callable, *args) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(process_pool, func, *args)

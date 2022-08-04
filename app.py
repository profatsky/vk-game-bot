import asyncio
import warnings

from vkbottle.bot import Message

from loader import bot
from blueprints import bps
from blueprints.register import start
from database.create_tables import create_tables

for bp in bps:
    bp.load(bot)


@bot.on.private_message()
async def no_understand(message: Message):
    await start(message)


warnings.filterwarnings("ignore", category=Warning)
loop = asyncio.get_event_loop()

if __name__ == "__main__":
    print("Бот запущен!")
    loop.run_until_complete(create_tables())
    bot.run_forever()

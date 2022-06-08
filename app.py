from vkbottle.bot import Message

from loader import bot
from blueprints import bps
from blueprints.register import start
from database.db import create_tables

for bp in bps:
    bp.load(bot)


@bot.on.private_message()
async def no_understand(message: Message):
    await start(message)

if __name__ == "__main__":
    print("Бот запущен!")
    create_tables()
    bot.run_forever()

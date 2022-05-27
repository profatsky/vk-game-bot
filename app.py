from vkbottle.bot import Message

from loader import bot
from blueprints import bps
from blueprints.register import start


for bp in bps:
    bp.load(bot)


@bot.on.private_message()
async def no_understand(message: Message):
    await start(message)


bot.run_forever()

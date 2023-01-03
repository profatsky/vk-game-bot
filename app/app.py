from vkbottle.bot import Message

from loader import bot
from blueprints import bps
from blueprints.register import start

for bp in bps:
    bp.load(bot)


@bot.on.private_message()
async def no_understand(message: Message):
    await start(message)


# warnings.filterwarnings("ignore", category=Warning)

def setup_app():
    print("Бот запущен!")
    bot.run_forever()

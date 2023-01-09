from loguru import logger
from tortoise import Tortoise

from config import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD, bot
from handlers import labelers


for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)


async def startup_task():
    await Tortoise.init(
        db_url='mysql://{user}:{password}@{host}/{database}'.format(
            user=DB_USER, password=DB_PASSWORD,
            host=DB_HOST, database=DB_NAME
        ),
        modules={'models': ['database.models']}
    )
    await Tortoise.generate_schemas()
    print('База данных подключена')


# warnings.filterwarnings("ignore", category=Warning)
logger.disable('vkbottle')

if __name__ == '__main__':
    bot.loop_wrapper.on_startup.append(startup_task())
    print('Бот запущен!')
    bot.run_forever()

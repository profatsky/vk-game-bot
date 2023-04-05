from tortoise import Tortoise

from config import bot
from handlers import labelers


for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)


async def startup_task():
    await Tortoise.init(
        db_url='sqlite://database/db.sqlite3?journal_mode=delete',
        modules={'models': ['database.models']}
    )
    print('База данных подключена')


if __name__ == '__main__':
    bot.loop_wrapper.on_startup.append(startup_task())
    print('Бот запущен!')
    bot.run_forever()

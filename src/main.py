from tortoise import Tortoise

from admin.utils import save_admin_list, appoint_superuser
from core.loader import bot
from core.settings import MODELS
from core.handlers import labelers


for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)


async def startup_task():
    await Tortoise.init(
        db_url='sqlite://database/db.sqlite3?journal_mode=delete',
        modules={'models': MODELS}
    )
    print('База данных подключена')
    await appoint_superuser()
    await save_admin_list()


async def shutdown_task():
    await Tortoise.close_connections()
    print('Завершение работы')


if __name__ == '__main__':
    # logger.stop()
    bot.loop_wrapper.on_startup.append(startup_task())
    bot.loop_wrapper.on_shutdown.append(shutdown_task())
    print('Бот запущен!')
    bot.run_forever()

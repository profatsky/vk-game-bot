from concurrent.futures import ProcessPoolExecutor

from vkbottle import Bot, CtxStorage, PhotoMessageUploader
from vkbottle.framework.labeler import BotLabeler

from core.settings import TOKEN

labeler = BotLabeler()

bot = Bot(
    token=TOKEN,
    labeler=labeler
)

photo_message_uploader = PhotoMessageUploader(bot.api)

admin_list = CtxStorage()

process_pool = ProcessPoolExecutor()

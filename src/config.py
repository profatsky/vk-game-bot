import os

from dotenv import load_dotenv
from vkbottle import Bot, CtxStorage
from vkbottle.framework.labeler import BotLabeler

load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

labeler = BotLabeler()
bot = Bot(
    token=TOKEN,
    labeler=labeler
)

admin_list = CtxStorage()

MODELS = [
    'users.models',
    'mining.models',
    'income.models',
    'admin.models',
    'aerich.models'
]

DATABASE_CONFIG = {
    'connections': {
        'default': 'sqlite://src/database/db.sqlite3?journal_mode=delete'
    },
    'apps': {
        'models': {
            'models': MODELS,
            'default_connection': 'default',
        }
    },
}

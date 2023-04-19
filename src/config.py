import os

from dotenv import load_dotenv
from vkbottle import Bot
from vkbottle.framework.labeler import BotLabeler

load_dotenv()
TOKEN = os.getenv("TOKEN")

labeler = BotLabeler()
bot = Bot(
    token=TOKEN,
    labeler=labeler
)

DATABASE_CONFIG = {
    'connections': {
        'default': 'sqlite://src/database/db.sqlite3?journal_mode=delete'
    },
    'apps': {
        'models': {
            'models': ['database.models', 'aerich.models'],
            'default_connection': 'default',
        }
    },
}

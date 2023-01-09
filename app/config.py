import os

from dotenv import load_dotenv
from vkbottle import Bot
from vkbottle.framework.labeler import BotLabeler

load_dotenv()
TOKEN = os.getenv("TOKEN")

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

labeler = BotLabeler()
bot = Bot(
    token=TOKEN,
    labeler=labeler
)

DATABASE_CONFIG = {
    'connections': {
        'default': 'mysql://{user}:{password}@{host}/{database}'.format(
            user=DB_USER, password=DB_PASSWORD,
            host=DB_HOST, database=DB_NAME
        )
    },
    'apps': {
        'models': {
            'models': ['app.database.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}

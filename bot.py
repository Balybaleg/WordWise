import logging
import settings

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

TELGERAM_API_TOKEN = settings.TELEGRAM_API_TOKEN


# Configure logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELGERAM_API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



print('WordWise Bot is working')

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
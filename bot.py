import asyncio
import logging
from tg_bot.config import load_config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tg_bot.keyboards.callbackdatas import diary_callback
from tg_bot.handlers.echo import register_create
from tg_bot.handlers.diaryhandler import register_start
logger = logging.getLogger(__name__)

def register_all_middlewares(dp):
    pass

def register_all_filters(dp):
    pass


def register_all_handlers(dp):
    register_create(dp)
    register_start(dp)



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format = u'%(filename)s'
    )
    config = load_config(".env")


    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot["config"] = config
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):



        logger.error("Bot stopped")
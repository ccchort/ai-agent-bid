import asyncio
import logging
from maxapi import Bot, Dispatcher
from config import config


logging.basicConfig(level=logging.INFO)


bot = Bot(config.max_bot_token.get_secret_value())
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
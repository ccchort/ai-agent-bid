import asyncio
import logging
from maxapi import Bot, Dispatcher
from config import config
from max.handlers.bid import bid


logging.basicConfig(level=logging.INFO)


bot = Bot(config.max_bot_token.get_secret_value())
dp = Dispatcher()

async def main():
    dp.include_routers(bid)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
from telegram.handlers.bid import bid
from aiogram.client.default import DefaultBotProperties
from database.db import DataBase

from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    db = DataBase()

    storage = MemoryStorage()


    #proxy_url = "socks5://192.168.0.10:1080"
    #session = AiohttpSession(proxy=proxy_url) if proxy_url else None
    bot = Bot(token=config.telegram_bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML), )#session=session)
    
    dp = Dispatcher(storage=storage)
    dp["db"] = db

    dp.include_routers(bid)    

    await dp.start_polling(bot)

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: print("EXIT")
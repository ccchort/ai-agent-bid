import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
from telegram.handlers.bid import bid
from aiogram.client.default import DefaultBotProperties
from database.db import DataBase

from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    db = DataBase()

    storage = MemoryStorage()


    CUSTOM_API_SERVER = TelegramAPIServer(
        base="https://lingering-mountain-4634.egorilyasov2006.workers.dev/bot{token}/{method}",
        file="https://lingering-mountain-4634.egorilyasov2006.workers.dev/bot{token}/{method}"
    )
    test_url = CUSTOM_API_SERVER.api_url(token=config.telegram_bot_token.get_secret_value(), method="getMe")
    print(f"DEBUG_BOT_URL: {test_url}", flush=True)
    session = AiohttpSession(api=CUSTOM_API_SERVER)
    bot = Bot(token=config.telegram_bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
    
    dp = Dispatcher(storage=storage)
    dp["db"] = db

    dp.include_routers(bid)    

    await dp.start_polling(bot)

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: print("EXIT")
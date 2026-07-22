import asyncio
import logging
from maxapi import Bot, Dispatcher
from config import config
from max.handlers.bid import bid


logging.basicConfig(level=logging.INFO)


bot = Bot(config.max_bot_token.get_secret_value())
dp = Dispatcher()

async def main():
    await bot.unsubscribe_webhook("https://im-ru.bitrix.info/imwebhook/eh/ad9211ded85099574d4a524f92825c441774023999/")
    subs = await bot.get_subscriptions()
    print(subs)
    dp.include_routers(bid)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try: asyncio.run(main())
    except KeyboardInterrupt: print("Stopped")
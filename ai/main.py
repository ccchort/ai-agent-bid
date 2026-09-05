import asyncio
import logging
import traceback
from config import config
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import text
from utils.collector import format_datetime
from utils.notify import make_message_to_managers
from database.db import DataBase
from database.models import UserSession
from ai.add_bid import generate
from ai.shit import insert_row_to_google_sheet

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
db = DataBase()




async def get_stale_user_sessions() -> list[dict]:
    """
    Проверяет `user_sessions.last_message_at` раз в минуту.
    """
    rows = await DataBase.get_from_db(
        UserSession,
        where_clauses=[
            UserSession.last_message_at < text("CURRENT_TIMESTAMP - INTERVAL '3 minutes'")
        ]
    )

    return [
        {
            "id": row.id,
            "user_id": row.user_id,
            "platform": row.platform,
            "accumulated_text": row.accumulated_text,
            "created_at": format_datetime(row.created_at),
            "last_message_at": format_datetime(row.last_message_at),
            "client_name": row.client_name,
        }
        for row in rows or []
    ]


async def check_user_sessions_job():
    stale_sessions = await get_stale_user_sessions()

    for session in stale_sessions:
        try:
            data = await generate(session)
            if not data:
                await db.delete_from_db(UserSession, filters={"user_id": session.get("user_id", None)})
                continue

            bot_token = config.telegram_bot_token.get_secret_value()
            manager_chat_id = config.manager_chat_id.get_secret_value()
            if bot_token and manager_chat_id:
                message = make_message_to_managers(data)
                request = Request(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    data=urlencode({"chat_id": manager_chat_id, "text": message}).encode(),
                    parse_mode="HTML", method="POST",
                )
                await asyncio.to_thread(urlopen, request)

            await insert_row_to_google_sheet(
                data,
                json_key_path="./ai/info/bids-project-502021-d03d48f79611.json",
                spreadsheet_name="Регистрация обращений клиентов (Ответы)"
            )
            await db.delete_from_db(UserSession, filters={"user_id": session.get("user_id", None)})

        except Exception:
            print(f"check_user_sessions_job failed for user_id={session.get('user_id')}")
            traceback.print_exc()



async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_user_sessions_job, "interval", seconds=30)
    scheduler.start()

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=False)
        print("Scheduler stopped.")


if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: print("Stopped")
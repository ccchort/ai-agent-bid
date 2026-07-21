from maxapi import F, Router
from maxapi.types import MessageCreated
from maxapi.filters import CommandStart
from database.db import DataBase
from database.models import UserSession
from sqlalchemy.sql import func

db = DataBase()
bid = Router()

@bid.message(CommandStart())
async def cmd_start(event: MessageCreated):
    await event.message.answer("Привет!")

@bid.message(F.message.body.text)
async def bid_msg(event: MessageCreated):
    accum_text = await db.get_from_db(UserSession, filters={"user_id": event.message.from_user.id})[0]
    await db.add_to_db(UserSession, 
                       {"user_id": event.message.from_user.id, 
                        "platform": "MAX", 
                        "accumulated_text": accum_text + event.message.text,
                        "last_message_at": func.now(),
                        "client_name": event.message.from_user.full_name})
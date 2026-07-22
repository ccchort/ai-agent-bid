from maxapi import F, Router
from maxapi.types import MessageCreated
from maxapi.filters.command import CommandStart
from database.db import DataBase
from database.models import UserSession
from sqlalchemy.sql import func

db = DataBase()
bid = Router()

@bid.message_created(CommandStart())
async def cmd_start(event: MessageCreated):
    await event.message.answer("Привет!")

@bid.message_created(F.message.body.text)
async def bid_msg(event: MessageCreated):
    accum_text = await db.get_from_db(UserSession, filters={"user_id": int(event.get_ids()[0])})
    if accum_text:
        accum_text = accum_text[0].accumulated_text
        await db.update_db(UserSession, 
                           filters={"user_id": int(event.get_ids()[0])}, 
                           update_data={"accumulated_text": accum_text + " " + event.message.body.text, "last_message_at": func.now()})
    else:
        await db.add_to_db(UserSession(user_id=int(event.get_ids()[0]), 
                        platform="Max",
                        accumulated_text=event.message.body.text,
                        last_message_at=func.now(),
                        client_name=event.from_user.full_name))
        
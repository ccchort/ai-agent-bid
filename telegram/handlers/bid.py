from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from database.db import DataBase
from database.models import UserSession
from sqlalchemy.sql import func

bid = Router()
db = DataBase()

@bid.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!")

@bid.business_message(F.text)
@bid.message(F.text)
async def bid_msg(message: Message):
    if message.from_user.id in [804843834, 1796987260, 6399035001]:
        return
    accum_text = await db.get_from_db(UserSession, filters={"user_id": int(message.from_user.id)})
    if accum_text:
        accum_text = accum_text[0].accumulated_text
        await db.update_db(UserSession,
                           filters={"user_id": int(message.from_user.id)}, 
                           update_data={"accumulated_text": accum_text + " " + message.text, "last_message_at": func.now()})
    else:
        await db.add_to_db(UserSession(user_id=int(message.from_user.id), 
                        platform="Telegram",
                        accumulated_text=message.text,
                        last_message_at=func.now(),
                        client_name=message.from_user.full_name))

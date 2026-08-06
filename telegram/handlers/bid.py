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

@bid.message(F.text)
@bid.message(F.photo)
@bid.message(F.document)
async def bid_msg(message: Message):
    if message.from_user.id in [804843834, 1796987260, 6399035001, 753650703]:
        return
    text = message.text if message.text else ""

    if message.photo:
        text += " Клиент прислал фото"
        if message.caption:
            text += message.caption
    elif message.document:
        text += " Клиент прислал файл"
        if message.caption:
            text += message.caption
    
    accum_text = await db.get_from_db(UserSession, filters={"user_id": int(message.from_user.id)})
    if accum_text:
        accum_text = accum_text[0].accumulated_text
        await db.update_db(UserSession,
                           filters={"user_id": int(message.from_user.id)}, 
                           update_data={"accumulated_text": accum_text + " " + text, "last_message_at": func.now()})
    else:
        await db.add_to_db(UserSession(user_id=int(message.from_user.id), 
                        platform="Telegram",
                        accumulated_text=text,
                        last_message_at=func.now(),
                        client_name=message.chat.title))

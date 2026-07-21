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
async def bid_msg(message: Message):
    accum_text = await db.get_from_db(UserSession, filters={"user_id": message.from_user.id})[0]
    await db.add_to_db(UserSession, 
                       {"user_id": message.from_user.id, 
                        "platform": "Telegram", 
                        "accumulated_text": accum_text + message.text,
                        "last_message_at": func.now(),
                        "client_name": message.from_user.full_name})
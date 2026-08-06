from maxapi import F, Router
from maxapi.types import MessageCreated
from maxapi.filters.command import CommandStart
from maxapi.types.message import MessageBody
from database.db import DataBase
from database.models import UserSession
from sqlalchemy.sql import func

db = DataBase()
bid = Router()

@bid.message_created(CommandStart())
async def cmd_start(event: MessageCreated):
    await event.message.answer("Привет!")

@bid.message_created(F.message.body.text)
@bid.message_created(F.message.body.attachments)
async def bid_msg(event: MessageCreated):
    user_id = event.message.sender.user_id if event.message.sender else None
    if user_id is None:
        return

    if user_id in [20814816, 236025600, 221618858, 107974518]:
        return

    accum_text = await db.get_from_db(UserSession, filters={"user_id": user_id})
    text = event.message.body.text if event.message.body.text else ""

    if event.message.body.attachments:
        text += "Клиент добавил вложение(фото или файл)"

    if accum_text:
        accum_text = accum_text[0].accumulated_text
        await db.update_db(
            UserSession,
            filters={"user_id": user_id},
            update_data={"accumulated_text": accum_text + " " + text, "last_message_at": func.now()},
        )
    else:
        await db.add_to_db(
            UserSession(
                user_id=user_id,
                platform="Max",
                accumulated_text=text,
                last_message_at=func.now(),
                client_name=event.chat.title,
            )
        )
        
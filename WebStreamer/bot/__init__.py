
from pyrogram import Client
from ..vars import Var

if Var.PHONE_NUMBER:
    bot_token = None
else:
    bot_token = Var.BOT_TOKEN

StreamBot = Client(
    session_name='Web Streamer',
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=bot_token,
    phone_number=Var.PHONE_NUMBER,
    sleep_threshold=Var.SLEEP_THRESHOLD,
    workers=Var.WORKERS
)

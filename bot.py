from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from os import getenv

# Replace with your own values
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
#PICS = (getenv('PICS', '')).split()

mxabot = Client('Mxa_Movies_Bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@mxabot.on_message(filters.command('start'))
def start(client, message):
    client.send_message(message.chat.id, 'Hᴇʟʟᴏ I Aᴍ @Mxa_Movies_Bot!\n\nI Cᴀɴ Sᴇᴀʀᴄʜ Mᴏᴠɪᴇs Oɴ Sᴇᴄɪғɪᴄ Wᴇʙsɪᴛᴇ\nJᴜsᴛ Sᴇɴᴅ Cᴏᴍᴍᴀɴᴅ Aɴᴅ Mᴏᴠɪᴇ Nᴀᴍᴇ')


mxabot.run()


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from os import getenv
from bs4 import BeautifulSoup
import requests
import re


API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
#PICS = (getenv('PICS', '')).split()

mxabot = Client('Mxa_Movies_Bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@mxabot.on_message(filters.command('start'))
def start(client, message):
    client.send_message(message.chat.id, 'Hᴇʟʟᴏ I Aᴍ @Mxa_Movies_Bot!\n\nI Cᴀɴ Sᴇᴀʀᴄʜ Mᴏᴠɪᴇs Oɴ Sᴇᴄɪғɪᴄ Wᴇʙsɪᴛᴇ\nJᴜsᴛ Sᴇɴᴅ Cᴏᴍᴍᴀɴᴅ Aɴᴅ Mᴏᴠɪᴇ Nᴀᴍᴇ')


def scrape(query):
    url = f"https://ww3.mkvcinemas.lat/?s={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    element = soup.find(class_=["ml-mask", "jt"])
    if element:
        href = element.get('href')
        title = element.get('oldtitle')
        thumbnail_tag = soup.find('img', {'class': 'mli-thumb'})
        thumbnail = thumbnail_tag['src'] if thumbnail_tag else None
        if title and href:
            return {'href': href, 'title': title, 'thumbnail': thumbnail}
    return None


@mxabot.on_message(filters.command('search'))
def search(client, message):
    try:
        query = message.text.split(' ', 1)[1].replace(' ', '+')
    except IndexError:
        message.reply_text("Please provide a search query.")
        return
    search_result = scrape(query)
    if search_result:
        caption = f"title: {search_result['title']}\nhref: {search_result['href']}"
        message.reply_text(caption)
    else:
        message.reply_text("No search results found.")



mxabot.run()


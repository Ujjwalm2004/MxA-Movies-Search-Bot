from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant
import os
from os import getenv
from bs4 import BeautifulSoup
import requests
import re
import time

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

mxabot = Client('Mxa_Movies_Bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
FSUB_CHANNEL = "Movies_X_Animes"

@mxabot.on_message(filters.command('start'))
def start(client, message):
    if FSUB_CHANNEL:
        try:
            user = client.get_chat_member(FSUB_CHANNEL, message.from_user.id)
            if user.status == "kicked out":
                message.reply_text("Sorry you are banned 🥲")
                return
        except UserNotParticipant:
            message.reply_text(
                text="Hey bruh you have to subscribe my update channel to use me",
                reply_markup=InlineKeyboardMarkup(
                [
                [
                   InlineKeyboardButton("Join Channel 📣", url=f"t.me/{FSUB_CHANNEL}")
                ],
                [
                    InlineKeyboardButton("Refresh 🔄", callback_data="refreshfsub")
                ]
            ]
        )
    )
            return

    start_msg = message.reply("▣ ▢ ▢")
    time.sleep(0.5)
    start_msg.edit_text(
       text="▣ ▣ ▢"
    )
    time.sleep(0.5)
    start_msg.edit_text(
       text="▣ ▣ ▣"
    )
    time.sleep(0.5)
    start_msg.edit_text(
       text="Hᴇʟʟᴏ I Aᴍ @Mxa_Movies_Bot!\n\nI Cᴀɴ Sᴇᴀʀᴄʜ Mᴏᴠɪᴇs Oɴ Sᴇᴄɪғɪᴄ Wᴇʙsɪᴛᴇ\nJᴜsᴛ Sᴇɴᴅ Cᴏᴍᴍᴀɴᴅ Aɴᴅ Mᴏᴠɪᴇ Nᴀᴍᴇ"
    )


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



@mxabot.on_message(filters.command("links"))
def get_links(client, message):
    url = message.text.split(" ", 1)[1]
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    gdlinks = soup.find_all("a", class_="gdlink")
    if gdlinks:
        pattern_480p = re.compile(r"\b480p\b", re.IGNORECASE)
        pattern_720p = re.compile(r"\b720p\b", re.IGNORECASE)
        pattern_1080p = re.compile(r"\b1080p\b", re.IGNORECASE)
        links = {"480p": [], "720p": [], "1080p": [], "Unknown": []}
        for link in gdlinks:
            href = link.get("href")
            title = link.get("title")
            if "s0" in title.lower():
                resolution = None
                if pattern_480p.search(title):
                    resolution = "480p"
                elif pattern_720p.search(title):
                    resolution = "720p"
                elif pattern_1080p.search(title):
                    resolution = "1080p"
                else:
                    resolution = "Unknown"
                links[resolution].append((title, href))


        if any(links.values()):
            for resolution, link_list in links.items():
                 if link_list:
                    response_msg = f"{resolution} links:\n"         
                    for i, (title, href) in enumerate(link_list, start=1):
                        response_msg += f"{i}. <a href='{href}'>{title}</a>\n"
                    message.reply_text(response_msg, disable_web_page_preview=True)
        else:
            response_msg = ""
            for i, gdlink in enumerate(gdlinks, start=1):
                title = gdlink.text.strip()
                hyperlink = gdlink["href"]
                response_msg += f'{i}. [{title}]({hyperlink})\n'
            message.reply_text(response_msg, disable_web_page_preview=True)
    else:
        all_links = soup.find_all("a", href=lambda href: href and "https://ww3.mkvcinemas.lat?" in href)
        response_msg = ""
        for i, link in enumerate(all_links, start=1):
            text = link.text.strip()
            hyperlink = link["href"]
            response_msg += f'{i}. [{text}]({hyperlink})\n'
        message.reply_text(response_msg, disable_web_page_preview=True)
 

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


@mxabot.on.callback_query()
async def callback(client, cmd: CallbackQuery):
    if cmd.data == "refreshfsub":
        rfrsh_msg = cmd.reply("Checking Please wait...")
    if FSUB_CHANNEL:
        try:
            user = client.get_chat_member(FSUB_CHANNEL, message.from_user.id)
            if user.status == "kicked out":
                cmd.reply_text("Sorry you are banned 🥲")
                return
        except UserNotParticipant:
            cmd.reply_text(
                text="Hey bruh you have to subscribe my update channel to use me",
                reply_markup=InlineKeyboardMarkup(
                [
                [
                   InlineKeyboardButton("Join Channel", url=f"t.me/{FSUB_CHANNEL}")
                ],
                [
                    InlineKeyboardButton("Contact Admin", url="t.me/iSmartBoiUjjwal_ib_bot")
                ]
            ]
        )
    )
            return
    rfrsh_msg.delete()
    new_msg = cmd.reply("Done You Are Subscriber of My Updates Channel")
    time.sleel(2)
    new_msg.edit_text("▣ ▢ ▢")
    time.sleep(0.5)
    new_msg.edit_text(
       text="▣ ▣ ▢"
    )
    time.sleep(0.5)
    new_msg.edit_text(
       text="▣ ▣ ▣"
    )
    time.sleep(0.5)
    new_msg.edit_text(
       text="Hᴇʟʟᴏ I Aᴍ @Mxa_Movies_Bot!\n\nI Cᴀɴ Sᴇᴀʀᴄʜ Mᴏᴠɪᴇs Oɴ Sᴇᴄɪғɪᴄ Wᴇʙsɪᴛᴇ\nJᴜsᴛ Sᴇɴᴅ Cᴏᴍᴍᴀɴᴅ Aɴᴅ Mᴏᴠɪᴇ Nᴀᴍᴇ",
       reply_markup=InlineKeyboardMarkup(
                [
                [
                   InlineKeyboardButton("Channel", url=f"t.me/{FSUB_CHANNEL}")
                ]
                ]
       )
    )


 

mxabot.run()


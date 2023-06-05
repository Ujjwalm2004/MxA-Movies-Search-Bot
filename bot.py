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


@mxabot.on_message(filters.command("mkv"))
def mkv_command(client: Client, message: Message):
    try:
        link = message.text.split(" ")[1]
        if "mkvcinemas" not in link:
            message.reply_text("Invalid link. Link must be of 'mkvcinemas.com'.")
            return
        process_message = message.reply_text("Processing link, please wait...", quote=True)
        with sync_playwright() as playwright:
            final_link = process_link(playwright, link, message)
        process_message.edit_text(f"Link processed successfully! \n{final_link}", disable_web_page_preview=True)
    except IndexError:
        message.reply_text("Please provide a valid link after the command. For example, `/mkv https://example.com`", quote=True)
    except Exception as e:
        message.reply_text(f"An error occurred while processing the link: {e}", quote=True)


@mxabot.on_message(filters.command("mkvc"))
def mkvcinemas(client: Client, message: Message):
    try:
        link = message.text.split(" ")[1]
        if "mkvcinemas" not in link:
            message.reply_text("Invalid link. Link must be of 'mkvcinemas.com'.")
            return
        process_message = message.reply_text("Processing link, please wait...", quote=True)
        response = requests.get(link)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        links = [a["href"] for a in soup.find_all("a", {"class": "gdlink"}, href=True)]

        final_links = []

        for link in links:
            if "mkvcinemas" in link:
                with sync_playwright() as playwright:
                    final_link = process_link(playwright, link, message)
                    title = soup.find("a", {"href": link, "class": "gdlink"}).text
                    final_link += f" - {title}\n"
                    final_links.append(final_link)
        final_links_text = "\n".join(final_links)
        links_per_message = 5
        final_links_chunks = [final_links[i:i+links_per_message] for i in range(0, len(final_links), links_per_message)]
        for i, links_chunk in enumerate(final_links_chunks):
            message_text = f"Links processed successfully! (Part {i+1}/{len(final_links_chunks)}) \n\n" + "\n".join(links_chunk)
            message.reply_text(message_text, disable_web_page_preview=True)
    except IndexError:
        message.reply_text("Please provide a valid link after the command. For example, `/mkv https://example.com`", quote=True)

    except Exception as e:
        # When an error occurs during the processing of the link
        message.reply_text(f"An error occurred while processing the link: {e}", quote=True)



mxabot.run()


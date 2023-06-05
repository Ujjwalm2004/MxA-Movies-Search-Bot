from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from os import getenv
from bs4 import BeautifulSoup
import requests
import re
from playwright.sync_api import Playwright, sync_playwright


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
def mkv_command(client, message):
    try:
        # Get the link from the message text
        link = message.text.split(" ")[1]
        # Check if the link contains "mkvcinemas"
        if "mkvcinemas" not in link:
            message.reply_text("Invalid link. Link must be of 'mkvcinemas.com'.")
            return
        # Send processing message
        process_message = message.reply_text("Processing link, please wait...", quote=True)
        with sync_playwright() as playwright:
            final_link = process_link(playwright, link, message)
        # Edit the process message with the final link
        process_message.edit_text(f"Link processed successfully! \n{final_link}", disable_web_page_preview=True)
    except IndexError:
        # When no link is provided in the message
        message.reply_text("Please provide a valid link after the command. For example, `/mkv https://example.com`", quote=True)
    except Exception as e:
        # When an error occurs during the processing of the link
        message.reply_text(f"An error occurred while processing the link: {e}", quote=True)


# Define the mkv_command function
@mxabot.on_message(filters.command("mkvc"))
def mkvcinemas(client, message):
    try:
        # Get the link from the message text
        link = message.text.split(" ")[1]
        # Check if the link contains "mkvcinemas"
        if "mkvcinemas" not in link:
            message.reply_text("Invalid link. Link must be of 'mkvcinemas.com'.")
            return
        # Send processing message
        process_message = message.reply_text("Processing link, please wait...", quote=True)
        # Use the requests library to get the HTML content of the link
        response = requests.get(link)
        html_content = response.text

        # Use BeautifulSoup to parse the HTML content and extract all links from the page
        soup = BeautifulSoup(html_content, "html.parser")
        links = [a["href"] for a in soup.find_all("a", {"class": "gdlink"}, href=True)]

        # Create an empty list to store the final links
        final_links = []
        # Loop through the links and process only those that contain "mkvcinemas" in the URL
        for link in links:
            if "mkvcinemas" in link:
                with sync_playwright() as playwright:
                    final_link = process_link(playwright, link, message)
                    # Extract the title of the link and append it to the final link
                    title = soup.find("a", {"href": link, "class": "gdlink"}).text
                    final_link += f" - {title}\n"
                    final_links.append(final_link)
        # Edit the process message with the final links
        final_links_text = "\n".join(final_links)
        # Split the final links into chunks of up to 10 links per message
        links_per_message = 5
        final_links_chunks = [final_links[i:i+links_per_message] for i in range(0, len(final_links), links_per_message)]
        for i, links_chunk in enumerate(final_links_chunks):
            # Send each chunk of links as a separate message
            message_text = f"Links processed successfully! (Part {i+1}/{len(final_links_chunks)}) \n\n" + "\n".join(links_chunk)
            message.reply_text(message_text, disable_web_page_preview=True)

    except IndexError:
        # When no link is provided in the message
        message.reply_text("Please provide a valid link after the command. For example, `/mkv https://example.com`", quote=True)
    except Exception as e:
        # When an error occurs during the processing of the link
        message.reply_text(f"An error occurred while processing the link: {e}", quote=True)



mxabot.run()


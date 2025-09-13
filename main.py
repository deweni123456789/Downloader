from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from modules.fb_downloader import download_fb_video
import config

app = Client("bot",
             api_id=config.API_ID,
             api_hash=config.API_HASH,
             bot_token=config.BOT_TOKEN)

# /start command
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text("👋 Hi! Send /fb <Facebook Video URL> to download a video.")

# /fb command
@app.on_message(filters.command("fb"))
async def fb_video_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Please provide a Facebook video URL.")

    url = message.command[1]
    msg = await message.reply_text("⏳ Downloading video...")

    video_data, filename = await download_fb_video(url)
    if not video_data:
        return await msg.edit("❌ Failed to download video.")

    await client.send_document(
        chat_id=message.chat.id,
        document=video_data,
        filename=filename,
        caption="✅ Here is your Facebook video!"
    )
    await msg.delete()

app.run()

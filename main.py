from pyrogram import Client, filters
from pyrogram.types import Message
from modules.fb_downloader import download_fb_video
import config

app = Client(
    "bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await message.reply_text(
        "👋 Hi! Send /fb <Facebook Video URL> to download a video."
    )

@app.on_message(filters.command("fb"))
async def fb_video_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Please provide a Facebook video URL.")
    
    url = message.command[1]
    msg = await message.reply_text("⏳ Downloading video...")

    try:
        video_file, meta = await download_fb_video(url)
        await client.send_document(
            chat_id=message.chat.id,
            document=video_file,
            caption="✅ Here is your Facebook video!"
        )
        await msg.delete()
    except Exception as e:
        await msg.edit(f"❌ Failed to download video:\n{e}")

app.run()

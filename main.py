from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules.fb_downloader import download_fb_video
import config

app = Client(
    "bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "👋 Hi! Send /fb <Facebook Video URL> to download and stream the video."
    )

@app.on_message(filters.command("fb"))
async def fb_video_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Please provide a Facebook video URL.")

    url = message.command[1]
    msg = await message.reply_text("⏳ Downloading video...")

    try:
        video_file, meta = await download_fb_video(url)
        user_mention = message.from_user.mention if message.from_user else "Anonymous"

        caption = f"""
🎬 <b>{meta.get('title')}</b>
⏳ Duration: {meta.get('duration')}

🙋‍♂️ Requested by: {user_mention}
🤖 Uploaded by: {config.BOT_NAME}
"""

        # Inline buttons in one row
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/deweni2"),
                InlineKeyboardButton("💬 Support Group", url="https://t.me/slmusicmania"),
                InlineKeyboardButton("📩 Contact Bot", url=f"https://t.me/{(await client.get_me()).username}")
            ]
        ])

        await client.send_video(
            chat_id=message.chat.id,
            video=video_file,
            caption=caption,
            width=meta.get("width"),
            height=meta.get("height"),
            thumb=meta.get("thumb"),
            reply_markup=buttons
        )

        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ Failed to download video:\n<code>{e}</code>")

app.run()

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from modules.fb_downloader import download_fb_video
import config

BOT_NAME = "EliZaBeth"

app = Client(
    "bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await message.reply_text(
        "👋 Hi! Send /fb <Facebook Video URL> to download and stream the video."
    )

@app.on_message(filters.command("fb"))
async def fb_video_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Please provide a Facebook video URL.")
    
    url = message.command[1]
    msg = await message.reply_text("⏳ Downloading video...")

    try:
        video_file, meta = await download_fb_video(url)

        # User mention
        user_mention = message.from_user.mention if message.from_user else "Anonymous"

        # Build caption
        caption = f"""
🎬 <b>{meta.get('title')}</b>
⏳ Duration: {meta.get('duration')}

👍 Likes: {meta.get('like_count')}
💬 Comments: {meta.get('comment_count')}
🔁 Shares: {meta.get('repost_count')}

📅 Uploaded Date: {meta.get('upload_date') or 'N/A'}
⏰ Uploaded Time: {meta.get('upload_time') or 'N/A'}

😊 Feeling: {meta.get('feeling')}
📍 Location: {meta.get('location')}
👤 Uploader: {meta.get('uploader')}

🙋‍♂️ Requested by: {user_mention}
🤖 Uploaded by: {BOT_NAME}
"""

        # Inline buttons (row type)
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/deweni2"),
                InlineKeyboardButton("💬 Support Group", url="https://t.me/slmusicmania"),
                InlineKeyboardButton("📩 Contact Bot", url=f"https://t.me/{(await client.get_me()).username}")
            ]
        ])

        # Send playable video
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

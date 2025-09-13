import yt_dlp
import tempfile
from io import BytesIO
import os

async def download_fb_video(url: str):
    """
    Downloads Facebook video using yt-dlp and returns BytesIO object and filename.
    """
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4",
        "quiet": True,
        "no_warnings": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    # Read video into memory
    with open(filename, "rb") as f:
        video_bytes = f.read()

    file = BytesIO(video_bytes)
    file.name = os.path.basename(filename)
    
    # Optional: remove temp file after reading
    os.remove(filename)

    return file

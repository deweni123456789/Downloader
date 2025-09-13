import yt_dlp
import os
import tempfile

async def download_fb_video(url: str):
    # Create a temp file to save video
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    
    # Read video bytes
    with open(filename, "rb") as f:
        video_bytes = f.read()

    return video_bytes, os.path.basename(filename)

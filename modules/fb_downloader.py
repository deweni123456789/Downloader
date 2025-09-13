import yt_dlp
import tempfile
from io import BytesIO
import os
from datetime import datetime

async def download_fb_video(url: str):
    """
    Downloads a Facebook video using yt-dlp and returns:
    - BytesIO video file
    - metadata dict
    """
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "writethumbnail": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    # Load video
    with open(filename, "rb") as f:
        video_bytes = f.read()

    file = BytesIO(video_bytes)
    file.name = os.path.basename(filename)

    # Thumbnail
    thumb = None
    try:
        thumb_path = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".jpg"
        if os.path.exists(thumb_path):
            thumb = thumb_path
    except:
        pass

    # Format duration
    def format_duration(sec):
        if not sec:
            return "N/A"
        m, s = divmod(int(sec), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

    # Metadata
    meta = {
        "title": info.get("title", "Facebook Video"),
        "duration": format_duration(info.get("duration")),
        "width": info.get("width"),
        "height": info.get("height"),
        "upload_date": None,
        "upload_time": None,
        "like_count": info.get("like_count", "N/A"),
        "comment_count": info.get("comment_count", "N/A"),
        "repost_count": info.get("repost_count", "N/A"),
        "location": info.get("location", "N/A"),
        "uploader": info.get("uploader", "N/A"),
        "feeling": info.get("chapters", "N/A"),  # yt-dlp often doesn't give "feeling"
        "thumb": thumb
    }

    # Format date/time
    if info.get("upload_date"):
        try:
            dt = datetime.strptime(info["upload_date"], "%Y%m%d")
            meta["upload_date"] = dt.strftime("%Y-%m-%d")
            meta["upload_time"] = dt.strftime("%H:%M:%S")
        except:
            pass

    # Cleanup video file
    os.remove(filename)

    return file, meta

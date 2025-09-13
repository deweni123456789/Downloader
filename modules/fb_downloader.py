import yt_dlp
import tempfile
from io import BytesIO
import os

MAX_FILENAME_LEN = 100  # truncate filenames to 100 characters

async def download_fb_video(url: str):
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")

    def sanitize_filename(d):
        # Limit length of filename
        title = d.get("title", "video")
        if len(title) > MAX_FILENAME_LEN:
            d["title"] = title[:MAX_FILENAME_LEN]
        return d

    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "writethumbnail": True,
        "progress_hooks": [],
        "postprocessors": [],
        "playlist_items": "1",
        "extract_flat": False,
        "noplaylist": True,
        "logger": None,
        "merge_output_format": "mp4",
        "before_dl_hook": sanitize_filename  # modify title before download
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
        except Exception as e:
            raise Exception(f"yt-dlp failed: {e}")

        # Truncate filename if needed
        filename = ydl.prepare_filename(info)
        if len(filename) > 255:
            filename = filename[:255]

        if not os.path.exists(filename):
            raise Exception("Video file not found after download!")

    # Load video
    with open(filename, "rb") as f:
        video_bytes = f.read()
    if not video_bytes:
        raise Exception("Downloaded video is empty!")

    file = BytesIO(video_bytes)
    file.name = os.path.basename(filename)

    # Thumbnail
    thumb = None
    try:
        thumb_path = filename.rsplit(".", 1)[0] + ".jpg"
        if os.path.exists(thumb_path):
            thumb = thumb_path
    except:
        pass

    # Duration formatter
    def format_duration(sec):
        if not sec:
            return "N/A"
        m, s = divmod(int(sec), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

    meta = {
        "title": info.get("title", "Facebook Video")[:MAX_FILENAME_LEN],
        "duration": format_duration(info.get("duration")),
        "width": info.get("width"),
        "height": info.get("height"),
        "thumb": thumb
    }

    try:
        os.remove(filename)
    except:
        pass

    return file, meta

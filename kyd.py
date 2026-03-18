#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title kyd
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 😸
# @raycast.packageName kitty youtube downloader
# @raycast.description 🐾 kitty MP3/MP4 youtube downloader
# @raycast.argument1 { "type": "text", "placeholder": "URL" }
# @raycast.argument2 { "type": "text", "placeholder": "MP3/MP4" }

import sys
import os
from yt_dlp import YoutubeDL

url = sys.argv[1]
ext = sys.argv[2]

def get_metadata(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            metadata = {
                "Title": info.get('title'),
                "Author": info.get('uploader'),
                "Duration": info.get('duration') # seconds
            }

            return metadata
    
    except Exception as e:
        print(f"[!] Something went wrong while fetching metadata: {e}")
        return None

data = get_metadata(url)

def download_data(url, ext, data):
    working_dir = os.path.dirname(__file__)
    out_path = os.path.expanduser("~/Videos/kyd_output")

    ext = ext.lower()

    if ext == "mp3":
        ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'noprogress': True,
                'format': "bestaudio/best",
                'outtmpl':{'default': '%(title)s.%(ext)s'},
                'paths': {'home': out_path},
                'ffmpeg_location': os.path.join(working_dir, "ffmpeg.exe"),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': ext
                }]
        }
        

    elif ext == "mp4": 
        ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'noprogress': True,
                'format': "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
                'outtmpl':{'default': '%(title)s.%(ext)s'},
                'merge_output_format': ext,
                'ffmpeg_location': os.path.join(working_dir, "ffmpeg.exe"),
                'paths': {'home': out_path } 
        }
            
    else:
        print("[!] Unknown format")
        return


    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        if data:
            print(f"\n[+] Done: {data['Title']}\n [dir] {out_path}")
        else:
            print(f"[+] Done\n [dir] {out_path}")


if data:
    print(f"[+] Downloading: {data['Title']}")
else:
    print("[+] Downloading...")

download_data(url, ext, data)
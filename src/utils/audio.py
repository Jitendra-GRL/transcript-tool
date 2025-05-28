import yt_dlp
import os
import subprocess
import tempfile
import logging

def download_audio(url):
    """Download audio from YouTube video"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info).replace('.webm', '.mp3')
        return audio_file

def extract_audio_segment(input_file, start_time, duration, output_file):
    """Extract a segment of audio from the input file."""
    command = f'ffmpeg -i "{input_file}" -ss {start_time} -t {duration} -acodec copy "{output_file}"'
    exit_code = subprocess.call(command, shell=True)
    if exit_code != 0:
        raise RuntimeError(f"Failed to extract audio segment from {input_file}")
    logging.info(f"Extracted audio segment to {output_file}")
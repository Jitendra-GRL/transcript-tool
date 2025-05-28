import os
import ffmpeg
from math import ceil
import logging
import subprocess

def split_audio(audio_file, chunk_size=300):
    """Split audio file into chunks of specified size"""
    try:
        logging.info(f"Probing audio file: {audio_file}")
        probe = ffmpeg.probe(audio_file)
        duration = float(probe['format']['duration'])
    except ffmpeg.Error as e:
        logging.error(f"FFmpeg probe failed: {str(e)}")
        logging.error(f"FFmpeg stderr: {e.stderr.decode('utf-8')}")  # Log the stderr
        raise

    chunks = []
    chunk_dir = "chunks"
    os.makedirs(chunk_dir, exist_ok=True)

    # Calculate chunks
    num_chunks = ceil(duration / chunk_size)

    for i in range(num_chunks):
        start_time = i * chunk_size
        output_file = os.path.join(chunk_dir, f"chunk_{i}.mp3")

        try:
            logging.info(f"Creating chunk {i}: {output_file}")
            # Construct the FFmpeg command as a list of strings
            command = [
                'ffmpeg',
                '-ss', str(start_time),
                '-t', str(chunk_size),
                '-i', audio_file,
                '-vn',  # Disable video
                '-acodec', 'libmp3lame',  # Use MP3 encoder
                '-ac', '2',  # Set to stereo
                '-ab', '192k',  # Set bitrate
                output_file
            ]

            # Execute the command using subprocess
            process = subprocess.Popen(command, stderr=subprocess.PIPE)
            _, stderr = process.communicate()

            if process.returncode != 0:
                logging.error(f"FFmpeg chunking failed with return code {process.returncode}")
                logging.error(f"FFmpeg stderr: {stderr.decode('utf-8')}")
                continue

            chunks.append(output_file)
        except Exception as e:
            logging.error(f"FFmpeg chunking failed: {str(e)}")
            continue

    return chunks
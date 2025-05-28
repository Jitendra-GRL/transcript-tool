# settings.py

# Configuration settings for the YouTube Transcript Fetcher project

API_KEY = "your_api_key_here"  # Replace with your actual API key
VIDEO_URL = "https://www.youtube.com/watch?v=your_video_id_here"  # Replace with the YouTube video URL
TEMP_AUDIO_DIR = "temp_audio"  # Directory for temporary audio files
TRANSCRIPT_OUTPUT_FILE = "transcript.txt"  # Output file for the final transcript
CHUNK_SIZE = 5  # Size of audio chunks in seconds
LOG_FILE = "transcription.log"  # Log file for recording the transcription process
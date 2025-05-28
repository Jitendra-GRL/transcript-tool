import argparse
from utils.audio import download_audio
from utils.chunking import split_audio
from utils.transcription import transcribe_chunks
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('transcription.log'),
            logging.StreamHandler()
        ]
    )

def main():
    parser = argparse.ArgumentParser(description='YouTube Video Transcriber')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--chunk-size', type=int, default=300, 
                       help='Chunk size in seconds (default: 300)')
    parser.add_argument('--model-size', type=str, default='large-v3',
                        help='Whisper model size (default: large-v3)')
    args = parser.parse_args()

    setup_logging()
    
    try:
        # Download audio
        logging.info("Downloading audio from YouTube...")
        audio_file = download_audio(args.url)

        # Split into chunks
        logging.info("Splitting audio into chunks...")
        chunks = split_audio(audio_file)

        # Transcribe chunks
        logging.info("Transcribing chunks...")
        transcript = transcribe_chunks(chunks, model_size=args.model_size)

        # Save transcript
        output_file = "transcript.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        logging.info(f"Transcript saved to {output_file}")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
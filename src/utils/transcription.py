from faster_whisper import WhisperModel
import logging
from tqdm import tqdm
import os
import torch
from concurrent.futures import ThreadPoolExecutor, as_completed

class TranscriptionManager:
    def __init__(self, model_size="large-v3", device="cuda" if torch.cuda.is_available() else "cpu"):
        """
        Initialize the transcription manager
        model_size options: tiny, base, small, medium, large-v1, large-v2, large-v3
        """
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type="float16" if device == "cuda" else "float32"
        )
        logging.info(f"Initialized {model_size} model on {device}")

    def transcribe_chunk(self, audio_path):
        """Transcribe a single audio chunk"""
        try:
            segments, _ = self.model.transcribe(
                audio_path,
                beam_size=5,
                word_timestamps=True,
                vad_filter=True
            )
            
            text = ""
            for segment in segments:
                text += f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
            
            return text
        
        except Exception as e:
            logging.error(f"Error transcribing {audio_path}: {str(e)}")
            return ""

def transcribe_chunks(chunk_files, model_size="large-v3", max_workers=4, output_file="transcript.txt"):
    """Transcribe multiple audio chunks in parallel with progress tracking and write as soon as ready"""
    transcriber = TranscriptionManager(model_size=model_size)
    # Clear the output file at the start
    open(output_file, "w", encoding="utf-8").close()

    def transcribe_and_cleanup(chunk_file):
        chunk_transcript = transcriber.transcribe_chunk(chunk_file)
        if os.path.exists(chunk_file):
            os.remove(chunk_file)
        # Write this chunk's transcript immediately
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"\n=== New Chunk ===\n{chunk_transcript}")
        return None  # No need to collect transcripts in memory

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(transcribe_and_cleanup, chunk) for chunk in chunk_files]
        for _ in tqdm(as_completed(futures), total=len(chunk_files), desc="Transcribing chunks"):
            pass  # All writing is handled in the worker

    # Optionally, return the output file path
    return output_file
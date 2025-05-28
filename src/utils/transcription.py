from faster_whisper import WhisperModel
import logging
from tqdm import tqdm
import os
import torch

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

def transcribe_chunks(chunk_files, model_size="large-v3"):
    """Transcribe multiple audio chunks with progress tracking"""
    transcriber = TranscriptionManager(model_size=model_size)
    full_transcript = ""
    
    for chunk_file in tqdm(chunk_files, desc="Transcribing chunks"):
        try:
            chunk_transcript = transcriber.transcribe_chunk(chunk_file)
            full_transcript += f"\n=== New Chunk ===\n{chunk_transcript}"
            
            # Clean up chunk file
            if os.path.exists(chunk_file):
                os.remove(chunk_file)
                
        except Exception as e:
            logging.error(f"Failed to process chunk {chunk_file}: {str(e)}")
            continue
    
    return full_transcript
import os
from faster_whisper import WhisperModel

def transcribe_audio(file_path):
    if not file_path or not os.path.exists(file_path):
        raise ValueError("Invalid audio file path or file does not exist.")

    model = WhisperModel("base", device="cpu")  # <<< force CPU
    segments, _ = model.transcribe(file_path)
    return " ".join(segment.text for segment in segments)

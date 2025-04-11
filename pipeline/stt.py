import os
import whisper

def transcribe_audio(file_path):
    if not file_path or not os.path.exists(file_path):
        raise ValueError("Invalid audio file path or file does not exist.")

    model = whisper.load_model("large")
    result = model.transcribe(file_path)
    return result["text"]

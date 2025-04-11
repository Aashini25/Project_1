import gradio as gr
import os
from pipeline.stt import transcribe_audio
from pipeline.nlp import extract_entities
from pipeline.utils import save_output

def process_audio(audio_file):
    if audio_file is None or not os.path.exists(audio_file):
        raise ValueError("Invalid audio file path or file does not exist.")

    transcript = transcribe_audio(audio_file)
    output = extract_entities(transcript)
    save_output(output)
    return output

iface = gr.Interface(
    fn=process_audio,
    inputs=gr.Audio(type="filepath", label="Record your voice"),
    outputs="json",
    title="Client Requirement Extractor",
    description="Speak your hiring requirement and extract structured details."
)

if __name__ == "__main__":
    iface.launch()

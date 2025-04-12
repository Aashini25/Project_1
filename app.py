import gradio as gr
import os
from pipeline.stt import transcribe_audio
from pipeline.nlp import extract_entities
from pipeline.utils import save_output

def process_input(audio_file=None, text_input=""):
    # Priority: audio > text
    if audio_file and os.path.exists(audio_file):
        transcript = transcribe_audio(audio_file)
    elif text_input.strip():
        transcript = text_input.strip()
    else:
        return {"error": "Please provide either audio or text input."}

    output = extract_entities(transcript)
    save_output(output)
    return output

iface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Audio(type="filepath", label="Record your voice (optional)"),
        gr.Textbox(lines=2, placeholder="Or type your requirement here...", label="Type your input (optional)")
    ],
    outputs="json",
    title="Client Requirement Extractor",
    description="Speak or type your hiring requirement to extract structured details like role, skills, experience, and location."
)

if __name__ == "__main__":
    iface.launch()

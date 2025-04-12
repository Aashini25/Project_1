import gradio as gr
import os
from pipeline.stt import transcribe_audio
from pipeline.nlp import extract_entities
from pipeline.utils import save_output
from mongodb.query_db import query_candidates

def process_input(audio_file=None, text_input=""):
    # Priority: audio > text
    if audio_file and os.path.exists(audio_file):
        transcript = transcribe_audio(audio_file)
    elif text_input.strip():
        transcript = text_input.strip()
    else:
        return {"error": "Please provide either audio or text input."}

    # Step 1: Extract entities from text/audio
    extracted_info = extract_entities(transcript)

    # Step 2: Save extracted info (if needed for logging)
    save_output(extracted_info)

    # Step 3: Query MongoDB for matching candidates
    matching_profiles = query_candidates(extracted_info)

    # Step 4: Return both the requirement and results
    return {
        "Extracted Requirement": extracted_info,
        "Matching Candidates": matching_profiles
    }

iface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Audio(type="filepath", label="Record your voice (optional)"),
        gr.Textbox(lines=2, placeholder="Or type your requirement here...", label="Type your input (optional)")
    ],
    outputs="json",
    title="Client Requirement Extractor + Matcher",
    description="Speak or type your hiring requirement to extract structured details like role, skills, experience, and location — and see matching candidates from the database."
)

if __name__ == "__main__":
    iface.launch()

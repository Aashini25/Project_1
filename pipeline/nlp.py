import spacy
import difflib

nlp = spacy.load("en_core_web_sm")

# Add a list of common cities (you can expand this)
known_locations = ["Bangalore", "Chennai", "Mumbai", "Delhi", "Hyderabad", "Kolkata", "Pune", "Gurgaon", "Noida"]

def fuzzy_location_match(text):
    words = text.split()
    for word in words:
        match = difflib.get_close_matches(word, known_locations, n=1, cutoff=0.8)
        if match:
            return match[0]
    return None

def extract_entities(text: str) -> dict:
    doc = nlp(text)
    role, skills, experience, location = None, [], None, None

    for ent in doc.ents:
        if ent.label_ == "GPE":
            location = ent.text
        elif ent.label_ == "DATE":
            if "year" in ent.text.lower():
                experience = ent.text

    # Fallback location using fuzzy match if spaCy didn't catch anything
    if not location:
        location = fuzzy_location_match(text)

    # Very simple keyword matching (improve later)
    if "developer" in text.lower():
        role = "Developer"
    if "react" in text.lower():
        skills.append("React")
    if "angular" in text.lower():
        skills.append("Angular")

    return {
        "intent": detect_intent(text),
        "role": role,
        "skills": skills,
        "experience": experience,
        "location": location
    }

def detect_intent(text: str) -> str:
    if any(keyword in text.lower() for keyword in ["need", "looking", "hire", "require"]):
        return "HiringRequirement"
    return "Unknown"

import spacy
import difflib

nlp = spacy.load("en_core_web_sm")

# Known lists
known_locations = ["Bangalore", "Chennai", "Mumbai", "Delhi", "Hyderabad", "Kolkata", "Pune", "Gurgaon", "Noida", "Coimbatore"]
known_skills = ["Node", "React", "Angular", "Java", "Python", "AWS", "Django", "Spring", "Flask"]
known_roles = ["Developer", "Architect", "Manager", "Engineer", "Lead", "Consultant"]

def fuzzy_match(word, choices, cutoff=0.8):
    match = difflib.get_close_matches(word, choices, n=1, cutoff=cutoff)
    return match[0] if match else None

def extract_entities(text: str) -> dict:
    doc = nlp(text)
    role, skills, experience, location = None, [], None, None
    words = text.split()

    # Skill extraction (early to avoid using skill words as location)
    for word in words:
        skill = fuzzy_match(word, known_skills, cutoff=0.75)
        if skill and skill not in skills:
            skills.append(skill)

    # Named entity based extraction
    for ent in doc.ents:
        if ent.label_ == "GPE" and not location:
            if ent.text not in skills:  # avoid overlapping with skills
                location = ent.text
        elif ent.label_ == "DATE" and not experience:
            if "year" in ent.text.lower():
                experience = ent.text

    # Fallback location (if not already found and not overlapping with skills)
    if not location:
        for word in words:
            if word not in skills:
                loc = fuzzy_match(word, known_locations)
                if loc:
                    location = loc
                    break

    # Role extraction
    for r in known_roles:
        if r.lower() in text.lower():
            role = r
            break

    # Fallback experience (if not caught)
    if not experience:
        for i, word in enumerate(words):
            if word.isdigit():
                if i + 1 < len(words) and "year" in words[i + 1].lower():
                    experience = f"{word} years"
                    break

    return {
        "intent": detect_intent(text),
        "role": role,
        "skills": skills,
        "experience": experience,
        "location": location
    }

    doc = nlp(text)
    role, skills, experience, location = None, [], None, None

    # Named entity based extraction
    for ent in doc.ents:
        if ent.label_ == "GPE" and not location:
            location = ent.text
        elif ent.label_ == "DATE" and not experience:
            if "year" in ent.text.lower():
                experience = ent.text

    # Fallback location
    if not location:
        location = fuzzy_match(text, known_locations)

    # Role extraction
    for r in known_roles:
        if r.lower() in text.lower():
            role = r
            break

    # Skill extraction
    for word in text.split():
        skill = fuzzy_match(word, known_skills, cutoff=0.75)
        if skill and skill not in skills:
            skills.append(skill)

    # Experience fallback if not caught
    if not experience:
        for word in text.split():
            if word.isdigit():
                idx = text.split().index(word)
                if idx + 1 < len(text.split()) and "year" in text.split()[idx + 1].lower():
                    experience = f"{word} years"
                    break

    return {
        "intent": detect_intent(text),
        "role": role,
        "skills": skills,
        "experience": experience,
        "location": location
    }

def detect_intent(text: str) -> str:
    if any(keyword in text.lower() for keyword in ["need", "looking", "hire", "require", "want"]):
        return "HiringRequirement"
    return "Unknown"

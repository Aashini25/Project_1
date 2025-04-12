from .db_config import get_db_connection, COLLECTION_NAME
import difflib
from pipeline.nlp import known_skills  # Import known_skills from nlp.py

def fuzzy_match(word, choices, cutoff=0.8):
    match = difflib.get_close_matches(word, choices, n=1, cutoff=cutoff)
    return match[0] if match else None

def query_candidates(extracted_info):
    client, db = get_db_connection()
    collection = db[COLLECTION_NAME]

    experience_str = extracted_info.get("experience", "")
    print("Extracted experience:", experience_str)

    # Handle "more than X years" and make sure it matches correctly as an integer
    if isinstance(experience_str, int):
        experience = experience_str
    elif "more than" in experience_str.lower():
        try:
            experience = int(experience_str.split()[2])
        except ValueError:
            experience = 0
    else:
        try:
            experience = int(experience_str.split()[0])
        except ValueError:
            experience = 0

    print("Final experience for query:", experience)

    # Extracted skills using fuzzy matching
    skills = extracted_info.get("skills", [])
    skills_query = []
    for skill in skills:
        matched_skill = fuzzy_match(skill, known_skills)  # Use fuzzy matching for skills
        if matched_skill:
            skills_query.append(matched_skill)
    
    print("Skills query:", skills_query)

    # MongoDB query
    query = {
        "skills": {"$in": skills_query},  # Match any of the fuzzy-matched skills
        "location": extracted_info.get("location", ""),
        "experience": {"$gte": experience}
    }

    if extracted_info.get("role"):
        query["role"] = extracted_info["role"]

    print("MongoDB Query:", query)

    # Fetch matching candidates
    matching_candidates = list(collection.find(query).sort("experience", -1))

    print("Matching candidates:", matching_candidates)
    
    return matching_candidates

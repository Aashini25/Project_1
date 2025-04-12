# create_mongo_db.py
from pymongo import MongoClient
from db_config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Clear old data
collection.delete_many({})

# Insert updated sample data
sample_data = [
    {"name": "Arjun Mehta", "role": "Developer", "skills": ["React", "Node"], "experience": 5, "location": "Bangalore"},
    {"name": "Priya Raman", "role": "Architect", "skills": ["AWS", "Java"], "experience": 10, "location": "Chennai"},
    {"name": "Rohit Kapoor", "role": "Data Scientist", "skills": ["Python", "Machine Learning"], "experience": 3, "location": "Delhi"},
    {"name": "Sneha Iyer", "role": "Product Manager", "skills": ["Agile", "Leadership"], "experience": 7, "location": "Mumbai"},
    {"name": "Ananya Gupta", "role": "UI/UX Designer", "skills": ["Figma", "Sketch"], "experience": 4, "location": "Bangalore"},
    {"name": "Vikram Singh", "role": "Backend Developer", "skills": ["Node.js", "MongoDB"], "experience": 6, "location": "Pune"},
    {"name": "Kiran Rao", "role": "Frontend Developer", "skills": ["JavaScript", "React"], "experience": 3, "location": "Hyderabad"},
    {"name": "Manoj Pillai", "role": "DevOps Engineer", "skills": ["AWS", "Docker"], "experience": 5, "location": "Chennai"},
    {"name": "Neha Joshi", "role": "QA Engineer", "skills": ["Automation", "Selenium"], "experience": 2, "location": "Bangalore"},
    {"name": "Amit Das", "role": "Data Engineer", "skills": ["Python", "SQL"], "experience": 4, "location": "Delhi"}
]

collection.insert_many(sample_data)
print("Sample candidate data inserted.")

import json
from faker import Faker
import random

fake = Faker()

registers = 500

# List of faculties and corresponding courses
faculties_courses = {
    "Engineering": ["Computer Science", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering"],
    "Arts": ["Fine Arts", "Performing Arts", "Literature", "History", "Philosophy"],
    "Science": ["Physics", "Chemistry", "Biology", "Mathematics", "Geology"],
    "Business": ["Business Administration", "Marketing", "Finance", "Accounting", "Human Resources"],
    "Medicine": ["General Medicine", "Nursing", "Pharmacy", "Dentistry", "Public Health"],
    "Law": ["Corporate Law", "Criminal Law", "International Law", "Civil Law", "Environmental Law"]
}

# Create a dictionary to hold all the records
courses_records = {}

# Function to generate a random course record
def generate_course_record():
    faculty = random.choice(list(faculties_courses.keys()))
    course = random.choice(faculties_courses[faculty])
    return {
        "faculty": {"1": faculty},
        "course_name": {"1": course},
        "course_code": {"1": fake.bothify(text='???###')},  # Generate random course code
        "description": {"1": fake.text(max_nb_chars=200)},  # Generate a brief description
        "credits": {"1": str(random.randint(1, 5))},  # Random number of credits
        "instructor": {"1": fake.name()}  # Random instructor name
    }

# Generate 100 course records
for i in range(1, registers + 1):
    courses_records[str(i)] = generate_course_record()

# Save the generated course records to a courses.json file
with open('./data/courses.json', 'w') as file:
    json.dump(courses_records, file, indent=4)

print(f"{registers} course records have been saved to courses.json")

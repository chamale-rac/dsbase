import json
from faker import Faker
import random

fake = Faker()

# Define the number of teacher records to generate
registers = 1000

# Read the courses.json file
with open('./data/courses.json', 'r') as file:
    courses_data = json.load(file)

# Extract course codes into an array
course_codes = [course["course_code"]["1"] for course in courses_data.values()]

# Create a dictionary to hold all the teacher records
teacher_records = {}

# Generate teacher records
for i in range(1, registers + 1):
    record = {
        "dpi": {"1": fake.random_number(digits=6, fix_len=True)},
        "name": {"1": fake.first_name()},
        "number": {"1": fake.random_number(digits=8, fix_len=True)},
        "lastname": {"1": fake.last_name()},
        "email": {"1": fake.email()},
        "birthday": {"1": fake.date_of_birth().isoformat()},
        "address": {"1": fake.address()},
        "phone_number": {"1": fake.phone_number()},
        "career": {"1": fake.job()},
        "course_code": {"1": random.choice(course_codes)}  # Assign a random course code
    }
    teacher_records[str(i)] = record

# Save the generated teacher records to a teachers.json file
with open('./data/teachers.json', 'w') as file:
    json.dump(teacher_records, file, indent=4)

print(f"{registers} teacher records have been saved to teachers.json")

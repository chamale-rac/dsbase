import json
from faker import Faker

fake = Faker()

registers = 10000

# Create a dictionary to hold all the records
records = {}

careers = [
    "Computer Science",
    "Software Engineering",
    "Information Systems",
    "Computer Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Industrial Engineering",
    "Chemical Engineering",
    "Biomedical Engineering",
    "Environmental Engineering",
    "Aerospace Engineering",
    "Materials Engineering",
    "Nuclear Engineering",
    "Petroleum Engineering",
    "Mining Engineering",
    "Geological Engineering",
    "Geomatics Engineering",
    "Agricultural Engineering",
    "Biotechnology Engineering",
    "Food Engineering",
]

# Generate records
for i in range(1, registers + 1):
    record = {
        "dpi": {"1": fake.random_number(digits=6, fix_len=True)},
        "name": {"1": fake.first_name()},
        "number": {"1": fake.random_number(digits=8, fix_len=True)},
        "lastname": {"1": fake.last_name()},
        "birthday": {"1": fake.date_of_birth().isoformat()},
        "email": {"1": fake.email()},
        "address": {"1": fake.address()},
        "phone_number": {"1": fake.phone_number()},
        "career": {"1": fake.random_element(careers)}
    }
    records[str(i)] = record

# Save the generated records to a students.json file
with open('./data/students.json', 'w') as file:
    json.dump(records, file, indent=4)

print(f"{registers} student records have been saved to students.json")

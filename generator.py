import json
import os
from faker import Faker
import random

fake = Faker()


def generate_courses_data(output_dir, registers=500):
    faculties_courses = {
        "Engineering": ["Computer Science", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Chemical Engineering"],
        "Arts": ["Fine Arts", "Performing Arts", "Literature", "History", "Philosophy"],
        "Science": ["Physics", "Chemistry", "Biology", "Mathematics", "Geology"],
        "Business": ["Business Administration", "Marketing", "Finance", "Accounting", "Human Resources"],
        "Medicine": ["General Medicine", "Nursing", "Pharmacy", "Dentistry", "Public Health"],
        "Law": ["Corporate Law", "Criminal Law", "International Law", "Civil Law", "Environmental Law"]
    }

    courses_records = {}
    course_codes = []

    def generate_course_record():
        faculty = random.choice(list(faculties_courses.keys()))
        course = random.choice(faculties_courses[faculty])
        code = fake.bothify(text='???###')
        while code in course_codes:
            code = fake.bothify(text='???###')
        course_codes.append(code)
        return {
            "course_info": {
                "faculty": faculty,
                "course_name": course,
                "course_code": code,
            },
            "description": {
                "description": fake.text(max_nb_chars=200),
                "credits": str(random.randint(1, 5))
            },
            "instructor": {
                "instructor_name": fake.name()
            }
        }

    for _ in range(registers):
        key = fake.bothify(text='??????')
        courses_records[key] = generate_course_record()

    os.makedirs(output_dir, exist_ok=True)
    for key, record in courses_records.items():
        for column_family, data in record.items():
            file_path = os.path.join(output_dir, f"{column_family}.json")
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f)
            with open(file_path, 'r+') as f:
                column_data = json.load(f)
                column_data[key] = data
                f.seek(0)
                json.dump(column_data, f, indent=4)

    print(f"{registers} course records have been saved to {output_dir}")
    return course_codes


def generate_students_data(output_dir, registers=10000):
    careers = [
        "Computer Science", "Software Engineering", "Information Systems", "Computer Engineering", "Electrical Engineering",
        "Mechanical Engineering", "Civil Engineering", "Industrial Engineering", "Chemical Engineering", "Biomedical Engineering",
        "Environmental Engineering", "Aerospace Engineering", "Materials Engineering", "Nuclear Engineering", "Petroleum Engineering",
        "Mining Engineering", "Geological Engineering", "Geomatics Engineering", "Agricultural Engineering", "Biotechnology Engineering",
        "Food Engineering"
    ]

    records = {}
    student_keys = []

    for _ in range(registers):
        key = fake.bothify(text='??????')
        student_keys.append(key)
        record = {
            "personal_info": {
                "dpi": fake.random_number(digits=6, fix_len=True),
                "name": fake.first_name(),
                "lastname": fake.last_name(),
                "birthday": fake.date_of_birth().isoformat()
            },
            "contact_info": {
                "email": fake.email(),
                "address": fake.address(),
                "phone_number": fake.phone_number()
            },
            "academic_info": {
                "career": fake.random_element(careers),
                "number": fake.random_number(digits=8, fix_len=True)
            }
        }
        records[key] = record

    os.makedirs(output_dir, exist_ok=True)
    for key, record in records.items():
        for column_family, data in record.items():
            file_path = os.path.join(output_dir, f"{column_family}.json")
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f)
            with open(file_path, 'r+') as f:
                column_data = json.load(f)
                column_data[key] = data
                f.seek(0)
                json.dump(column_data, f, indent=4)

    print(f"{registers} student records have been saved to {output_dir}")
    return student_keys


def generate_teachers_data(output_dir, registers=1000):
    teacher_records = {}
    teacher_keys = []

    for _ in range(registers):
        key = fake.bothify(text='??????')
        teacher_keys.append(key)
        record = {
            "personal_info": {
                "dpi": fake.random_number(digits=6, fix_len=True),
                "name": fake.first_name(),
                "lastname": fake.last_name(),
                "birthday": fake.date_of_birth().isoformat()
            },
            "contact_info": {
                "email": fake.email(),
                "address": fake.address(),
                "phone_number": fake.phone_number()
            },
            "professional_info": {
                "career": fake.job(),
                "number": fake.random_number(digits=8, fix_len=True)
            }
        }
        teacher_records[key] = record

    os.makedirs(output_dir, exist_ok=True)
    for key, record in teacher_records.items():
        for column_family, data in record.items():
            file_path = os.path.join(output_dir, f"{column_family}.json")
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f)
            with open(file_path, 'r+') as f:
                column_data = json.load(f)
                column_data[key] = data
                f.seek(0)
                json.dump(column_data, f, indent=4)

    print(f"{registers} teacher records have been saved to {output_dir}")
    return teacher_keys


def generate_course_teacher_data(output_dir, course_codes, teacher_keys, registers=1000):
    course_teacher_records = {}

    for _ in range(registers):
        teacher_key = random.choice(teacher_keys)
        course_code = random.choice(course_codes)
        composite_key = f"{course_code}_{teacher_key}"
        record = {
            "assignment_info": {
                "role": "Instructor",
                "semester": random.choice(["Fall", "Spring", "Summer"]),
                "year": random.randint(2000, 2023)
            }
        }
        course_teacher_records[composite_key] = record

    os.makedirs(output_dir, exist_ok=True)
    for key, record in course_teacher_records.items():
        for column_family, data in record.items():
            file_path = os.path.join(output_dir, f"{column_family}.json")
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f)
            with open(file_path, 'r+') as f:
                column_data = json.load(f)
                column_data[key] = data
                f.seek(0)
                json.dump(column_data, f, indent=4)

    print(f"{registers} course_teacher records have been saved to {output_dir}")


def generate_course_student_data(output_dir, course_codes, student_keys, registers=5000):
    course_student_records = {}

    for _ in range(registers):
        student_key = random.choice(student_keys)
        course_code = random.choice(course_codes)
        composite_key = f"{course_code}_{student_key}"
        record = {
            "performance_info": {
                "grade": random.randint(50, 100),
                "attendance": f"{random.randint(75, 100)}%"
            }
        }
        course_student_records[composite_key] = record

    os.makedirs(output_dir, exist_ok=True)
    for key, record in course_student_records.items():
        for column_family, data in record.items():
            file_path = os.path.join(output_dir, f"{column_family}.json")
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f)
            with open(file_path, 'r+') as f:
                column_data = json.load(f)
                column_data[key] = data
                f.seek(0)
                json.dump(column_data, f, indent=4)

    print(f"{registers} course_student records have been saved to {output_dir}")


def generate_metadata(output_dir):
    metadata = {
        "version": 1,
        "tables": {
            "courses": {
                "column_families": ["course_info", "description", "instructor"],
                "max_versions": 3,
                "is_enabled": True
            },
            "students": {
                "column_families": ["personal_info", "contact_info", "academic_info"],
                "max_versions": 3,
                "is_enabled": True
            },
            "teachers": {
                "column_families": ["personal_info", "contact_info", "professional_info"],
                "max_versions": 3,
                "is_enabled": True
            },
            "course_student": {
                "column_families": ["performance_info"],
                "max_versions": 3,
                "is_enabled": True
            },
            "course_teacher": {
                "column_families": ["assignment_info"],
                "max_versions": 3,
                "is_enabled": True
            }
        },
        "whoami": "admin",
        "status": {
            "servers": ["Server1"],
            "servers_amount": 1
        }
    }

    os.makedirs(output_dir, exist_ok=True)
    metadata_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_path, 'w') as file:
        json.dump(metadata, file, indent=4)

    print(f"Metadata has been saved to {metadata_path}")


if __name__ == "__main__":
    base_output_dir = './bases/school'
    course_codes = generate_courses_data(
        os.path.join(base_output_dir, 'courses'), 80)
    student_keys = generate_students_data(
        os.path.join(base_output_dir, 'students'), 300)
    teacher_keys = generate_teachers_data(
        os.path.join(base_output_dir, 'teachers'), 20)
    generate_course_teacher_data(os.path.join(
        base_output_dir, 'course_teacher'), course_codes, teacher_keys, 80)
    generate_course_student_data(os.path.join(
        base_output_dir, 'course_student'), course_codes, student_keys, 500)
    generate_metadata(base_output_dir)

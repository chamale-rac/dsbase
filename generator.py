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

        record = {
            "course_info": {
                "faculty": {"1": faculty},
                "course_name": {"1": course},
                "course_code": {"1": code},
            },
            "description": {
                "description": {"1": fake.text(max_nb_chars=200)},
                "credits": {"1": str(random.randint(1, 5))}
            },
            "instructor": {
                "instructor_name": {"1": fake.name()}
            }
        }

        # Randomly omit some column families or qualifiers
        if random.random() > 0.8:
            del record["description"]["description"]
        if random.random() > 0.8:
            del record["description"]
        if random.random() > 0.8:
            del record["instructor"]

        # Randomly add versions for some qualifiers
        for column_family in record:
            for qualifier in record[column_family]:
                versions = random.randint(1, 3)
                if versions > 1:
                    record[column_family][qualifier] = {str(i): fake.text(
                        max_nb_chars=200) for i in range(1, versions + 1)}

        return record

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

    def generate_student_record():
        record = {
            "personal_info": {
                "dpi": {"1": fake.random_number(digits=6, fix_len=True)},
                "name": {"1": fake.first_name()},
                "lastname": {"1": fake.last_name()},
                "birthday": {"1": fake.date_of_birth().isoformat()}
            },
            "contact_info": {
                "email": {"1": fake.email()},
                "address": {"1": fake.address()},
                "phone_number": {"1": fake.phone_number()}
            },
            "academic_info": {
                "career": {"1": fake.random_element(careers)},
                "number": {"1": fake.random_number(digits=8, fix_len=True)}
            }
        }

        # Randomly omit some column families or qualifiers
        if random.random() > 0.8:
            del record["personal_info"]["dpi"]
        if random.random() > 0.8:
            del record["contact_info"]["email"]
        if random.random() > 0.8:
            del record["academic_info"]

        # Randomly add versions for some qualifiers
        for column_family in record:
            for qualifier in record[column_family]:
                versions = random.randint(1, 3)
                if versions > 1:
                    record[column_family][qualifier] = {str(i): fake.text(
                        max_nb_chars=200) for i in range(1, versions + 1)}

        return record

    for _ in range(registers):
        key = fake.bothify(text='??????')
        student_keys.append(key)
        records[key] = generate_student_record()

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

    def generate_teacher_record():
        record = {
            "personal_info": {
                "dpi": {"1": fake.random_number(digits=6, fix_len=True)},
                "name": {"1": fake.first_name()},
                "lastname": {"1": fake.last_name()},
                "birthday": {"1": fake.date_of_birth().isoformat()}
            },
            "contact_info": {
                "email": {"1": fake.email()},
                "address": {"1": fake.address()},
                "phone_number": {"1": fake.phone_number()}
            },
            "professional_info": {
                "career": {"1": fake.job()},
                "number": {"1": fake.random_number(digits=8, fix_len=True)}
            }
        }

        # Randomly omit some column families or qualifiers
        if random.random() > 0.8:
            del record["personal_info"]["dpi"]
        if random.random() > 0.8:
            del record["contact_info"]["email"]
        if random.random() > 0.8:
            del record["professional_info"]

        # Randomly add versions for some qualifiers
        for column_family in record:
            for qualifier in record[column_family]:
                versions = random.randint(1, 3)
                if versions > 1:
                    record[column_family][qualifier] = {str(i): fake.text(
                        max_nb_chars=200) for i in range(1, versions + 1)}

        return record

    for _ in range(registers):
        key = fake.bothify(text='??????')
        teacher_keys.append(key)
        teacher_records[key] = generate_teacher_record()

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

    def generate_course_teacher_record():
        teacher_key = random.choice(teacher_keys)
        course_code = random.choice(course_codes)
        composite_key = f"{course_code}_{teacher_key}"
        record = {
            "assignment_info": {
                "role": {"1": "Instructor"},
                "semester": {"1": random.choice(["Fall", "Spring", "Summer"])},
                "year": {"1": random.randint(2000, 2023)}
            }
        }

        # Randomly omit some qualifiers
        if random.random() > 0.8:
            del record["assignment_info"]["semester"]

        # Randomly add versions for some qualifiers
        for column_family in record:
            for qualifier in record[column_family]:
                versions = random.randint(1, 3)
                if versions > 1:
                    record[column_family][qualifier] = {str(i): fake.text(
                        max_nb_chars=200) for i in range(1, versions + 1)}

        return composite_key, record

    for _ in range(registers):
        composite_key, record = generate_course_teacher_record()
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

    def generate_course_student_record():
        student_key = random.choice(student_keys)
        course_code = random.choice(course_codes)
        composite_key = f"{course_code}_{student_key}"
        record = {
            "performance_info": {
                "grade": {"1": random.randint(50, 100)},
                "attendance": {"1": f"{random.randint(75, 100)}%"}
            }
        }

        # Randomly omit some qualifiers
        if random.random() > 0.8:
            del record["performance_info"]["attendance"]

        # Randomly add versions for some qualifiers
        for column_family in record:
            for qualifier in record[column_family]:
                versions = random.randint(1, 3)
                if versions > 1:
                    record[column_family][qualifier] = {str(i): fake.text(
                        max_nb_chars=200) for i in range(1, versions + 1)}

        return composite_key, record

    for _ in range(registers):
        composite_key, record = generate_course_student_record()
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
        os.path.join(base_output_dir, 'courses'), 8)
    student_keys = generate_students_data(
        os.path.join(base_output_dir, 'students'), 25)
    teacher_keys = generate_teachers_data(
        os.path.join(base_output_dir, 'teachers'), 3)
    generate_course_teacher_data(os.path.join(
        base_output_dir, 'course_teacher'), course_codes, teacher_keys, 20)
    generate_course_student_data(os.path.join(
        base_output_dir, 'course_student'), course_codes, student_keys, 1000)
    generate_metadata(base_output_dir)

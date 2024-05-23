from faker import Faker

# Initialize Faker
fake = Faker()

# Open the file in write mode
with open('./generator/users.txt', 'w') as file:
    # Generate and write 100 strings to the file
    for i in range(1, 101):
        row_id = i
        dpi = ''.join([str(fake.random_digit_not_null()) for _ in range(10)])
        line = f"TableA {row_id} personal dpi {dpi}\n"
        file.write(line)

print("Data has been written to users.txt")

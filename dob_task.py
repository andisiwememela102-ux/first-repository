# Initialize two lists to store our separated data
names_list = []
birthdates_list = []

# Open and read the file
with open("DOB.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.split()
        # Expect at least: first_name last_name birthdate...
        if len(parts) >= 3:
            name = parts[0] + " " + parts[1]
            birthdate = " ".join(parts[2:])
            names_list.append(name)
            birthdates_list.append(birthdate)

# Print section header for names
print("Name")
for name in names_list:
    print(name)

print()

# Print section header for dates of birth
print("Birthdate")
for date in birthdates_list:
    print(date)

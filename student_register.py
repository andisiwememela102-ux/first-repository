# Ask the user how many students are registering
num_students = int(input("How many students are registering: "))

# Open the file 'reg_form.txt' in write mode('w')
with open("reg_form.txt", "w") as file:
    # Create a loop that runs for that number of students
    for i in range(num_students):
        # Ask the user to enter the student ID number
        student_id = input(f"Enter the student ID number for student {i + 1}: ")

        # Write the ID number and a dotted line to the file
        file.write(f"{student_id} ............\n")

print("\nRegistration complete! 'reg_form.txt' has been created successfully.")
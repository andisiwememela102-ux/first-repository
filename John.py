# Prompt the user to enter their name and convert it to lowercase
name = input("Enter your name: ").lower()

# Initialize an empty list to store the incorrect names
incorrect_names = []

# Use a while loop to check if the input is NOT "John"
while name != 'john':
    # Add the incorrect name to the list
    incorrect_names.append(name)
    name = input("Enter your name: ").lower()

# Print the list of incorrect names
print(f"Incorrect names: {incorrect_names}")
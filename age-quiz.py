# Prompt the user to enter their age and store it in variable age
age = int(input("Please enter your age: ")) 

# Check if the age is 100 or greater
if age >= 100:
    print("Sorry, you're dead.")

 # Check if the age is between 65 and 99
elif age >= 65:
    print("Enjoy your retirement!")


# Check if the age is between 40 and 64
elif age >= 40:
    print("You are over the hill.")

# Check if the age is under 13
elif age < 13:
    print("You qualify for the kiddie discount.")

# Check if the age is exactly 21
elif age == 21:
    print("Congrats on your 21st!")

# if none of the above conditions are met, print output a default message
else:
    print("Age is but a number.")
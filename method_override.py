class Adult:
    """ A class representing an adult person.
    """

    def __init__(self, name, age, eye_color, hair_color):
        self.name = name
        self.age = age
        self.eye_color = eye_color
        self.hair_color = hair_color

    def can_drive(self):
        """ Print that the adult is old enough to drive.
        """
        print(f"{self.name} is old enough to drive.")

class Child(Adult):
    """A subclass representing a child, inheriting from Adult.
    """        
    def can_drive(self):
        """ Overrides the parent class method to reflect child driving restrictions
        """
        print(f"{self.name} is too young drive.")


print("--- Person Registration System ---")

# Capture user inputs
user_name = input("Enter name: ").strip()

#Defensive exception handling to ensure age is entered as an integer
while True:
    try:
        user_age = int(input("Enter age: "))
        break
    except ValueError:
        print("Invalid input. Please enter a valid number for age.")

user_hair = input("Enter hair color: ").strip()
user_eye = input("Enter eye color: ").strip()

print("\n--- Processing Results ---")

# Control logic to determine which class to instantiate
if user_age >= 18:
    person = Adult(name=user_name, age=user_age, eye_color=user_eye, hair_color=user_hair)
else:
    person = Child(name=user_name, age=user_age, eye_color=user_age, hair_color=user_hair)

person.can_drive()        
        
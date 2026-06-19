"""
This program illustrate a logical error.
The time machine will calculate the current year and birth year
The logical error will occur when the calculations are in backwards,
"You are -21 years old", but instead, it outputs "You are 21 years old".

"""
print(f"Welcome to the Time machine!")

current_year = 2026
birth_year = 2005

age = birth_year - current_year  # Logical error, the calculations are backwards

print(f"You are", age, "years old.")
print(f" The time machine says you are getting younger!")
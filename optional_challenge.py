"""
This is program demonstrate types of errors

Errors and their types
1.Runtime Error : Can only concatenated strings to strings, not integers to strings.
2.Logical Error : the quotes around string '23' converts to integers.

"""


# Runtime Errors: Concatenated strings to strings, not integers to strings
# This will raise runtime error because Integers to Strings is not allowed.
name = "Andy"
age = 21
print(f"Hello" + name + "You are" + age + "years old.")

#Runtime Error : TypeError '>' is not supported between instance of 'str' and 'int'
#This will cause an error because it should be  integer not string
comp = "21 degrees" > 15

#Logical Error : The quotes around string '23'
# This will raise logical error because the age is not in integer, the output would be the age multiply by 10,
# instead of 230
# converts age to string 
age = "23"
month_age = age * 10
print(f"You will be" + (month_age) + "months old if you are" + age + "years old.")



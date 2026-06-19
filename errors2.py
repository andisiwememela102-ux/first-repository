"""
 
This example program demonstrate types of errors

#Types of Errors
1.Syntax error: There is a missing quotations around the string 'Lion'
2.Syntax error: Missing parenthesis in 'print Full_spec'
3.Logical error: There is an incorrect format string, Must use f-strings to easily format the strings. 
4.Logical error: Incorrect map variables to placeholders.

"""
#Added qoutes to make it a string.
animal = "Lion"
animal_type = "cub"
number_of_teeth = 16

#Fixed: Correct format string and a correct map variable placeholders.
full_spec =(f"This is a {animal}. It is a {number_of_teeth} and it has {animal_type} teeth.")

print("full_spec")


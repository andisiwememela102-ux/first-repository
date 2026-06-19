# This example program is meant to demonstrate errors.
 
#Syntax error: This error was returned 
#because the string statement was not enclosed in parenthesis.
print("Welcome to the error program")

#Syntax error: the error occured because
#this line was not enclosed in parenthesis
#Unexpected indentation
print ("\n")

#Syntax error : Unexpected indentation.
#Runtime error: There is an error because of "==" instead "="
#Fixed the the indetation and the removed the second "="
age_Str = "24 years old"

#Syntax error: Unexpected indentation.
#"age_Str" is not defined.
#Runtime error: ValueError returned as "years old"
#Fixed : Fixed the indentation, defined the "age_Str", Removed the last 9 chars and coverted to int.
age = int(age_Str[:-9]) 

#Syntax error : Unexpected indentation.
#Runtime error : string "age"  is incorrect we can only use Strings to Strings
#Fixed : fixed the indentation and converted age to string.
print("I'm" + str(age) + "years old.")

#Syntax error: Unexpected indentation.
#Fixed : Removed quotation to assign an integer to string.
years_from_now = 3


#Syntax error: Unexpected indentation.
#Runtime error: String "age"  is incorrect we can only use Strings to Strings
#not integers to Strings.
#Snytax errors :  the string statement is not enclosed in parenthesis.
#Syntax errors : incorrect string "answer_years" instead of "total_years".
#Fixed : fixed the indentation, fixed strings correctly, and converted total_years to string.
total_years = age + years_from_now
print("The total number of years:" + str(total_years))

#Syntax error: The string statement is not enclosed in parenthesis.
#Runtime error: Can not concatenate strings and integers.
#Logical error: 6 months was not added  to the total months.
#Fixed: concatenate strings correctly, and converted the total_months to integer, and added 6 months.
total_months = total_years * 12
print ("In 3 years and 6 months, I'll be " + str(total_months + 6) + " months old")


# Ask the user to enter a sentence
str_manipulation = input("Enter a sentence: ")

# Calculate and display the length of the sentence
length = len(str_manipulation)
print(f"The length of the sentence is: {length}")


#find the last letter in str_manipulation and replace every occurrence
#of that letter with '@'
last_letter = str_manipulation[-1]
str_replaced = str_manipulation.replace(last_letter, '@')
print(f"Sentence after replacing '{last_letter}' with '@': {str_replaced}")

# Print the last 3 characters in str_manipulation
last_three_reversed = str_manipulation[-3:][::-1]
print(f"The last 3 characters in reverse order are: {last_three_reversed}")

# create a five-letter word using the first first three letters of str_manipulation and the last two letters of str_manipulation
five_letter_word = str_manipulation[:3] + str_manipulation[-2:]
print(f"The new five-letter word is: {five_letter_word}")
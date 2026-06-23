print("Practical Task 1 : Part 1 : Alternating letters to upper and lowercase")

sentence = input("Enter a sentence: ")

#This program alternates each character into upper and lowercase in a sentence.

#Create an empty string
result = ""

#Loop through each character using its index 
for index in range(len(sentence)):
    #Convert letter to lowercase if index is even
    if index % 2 == 0:
        result += sentence[index].upper()#type:ignore
    #Convert letter to uppercase if index is odd   
    else:
        result += sentence[index].lower()#type:ignore
#Pint the modified string          
print(result)

print("Practical Task 1 : Part 2 : arlternating words to upper and lowercase ")

#Prompt the user for input
word_string = input("Enter a sentence: ")

#This program alternates each word into lower and uppercase in a sentence.

#Split the original string into words
words = word_string.split()

#Create an empty list
word_result_list = []

#Use for loops with enumerate to easily get the index and word from words
for index in range(len(words)):
    if index % 2 == 0:
    #Convert word to lowercase if index is even
     word_result_list.append(words[index].lower())
else:
   #Convert word to uppercase if index is odd
   word_result_list.append(words[index].upper())

#Turn the new word into a string
word_result = " ".join(word_result_list)

#Print the results
print(" ".join(word_result))


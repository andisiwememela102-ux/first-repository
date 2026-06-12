# Take the name of the user's favorite resturant 
string_favorite_restaurant = input("Enter the name of your favorite restaurant: ")


#take the uswer's favorite number
number_favorite = input("Enter your favorite number: ")


# Print the name of the restaurant and the number
print("Your favorite restaurant is: " + string_favorite_restaurant)
print("Your favorite number is: " + number_favorite)


#try to cast a string to an integer


int(string_fav)


'''This will cause an error because string_favorite_restaurant is a string and cannot be converted to an integer
Integers convert strings that represent numbers,
 and if the string contains non-numeric characters, it will raise a ValueError. 
it cannot be converted to an integer.'''

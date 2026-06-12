# prompt the user to enter three numbers
num1 = int(input("Enter the first number:"))
num2 = int(input("Enter the second number:"))
num3 = int(input("Enter the third number:"))

# Calculate the total of the three numbers
total_sum = num1 + num2 + num3

# Calculate the difference between the first and second numbers
difference = num1 - num2

# Calculate the product of the third number and the first number
product = num3 * num1

# Calculate the division of the total sum by the third number
division = total_sum / num3


# Display the results
print("Total sum:",total_sum)
print("Total difference:",difference)
print("Total product:",product)
print("Total division:",division)
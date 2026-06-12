# Ask the user to enter the length of the three sides of a triangle
import math


side1 = float(input("Enter the length of the first side of the triangle: "))
side2 = float(input("Enter the length of the second side of the triangle: "))
side3 = float(input("Enter the length of the third side of the triangle: "))


# Calculate the semi-perimeter of the triangle
semi_perimeter = (side1 + side2 + side3) / 2

# Calculate the area of the triangle using Heron's formula
area = math.sqrt(semi_perimeter * (semi_perimeter - side1) * (semi_perimeter - side2) * (semi_perimeter - side3))

# Display the perimeter and area of the triangle
print(f"The area of the triangle is: {area}")


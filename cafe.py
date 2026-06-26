# This program calculates the total value of the stock of my Cafe

# Create a list called Menu 
menu = ["coffee", "cake", "cheese cake", "croissant"]

# Create a dictionary called stock for the stock  value of each item stock
stock = {
     "coffee": 200,
     "cake": 150 ,
     "cheese cake": 50,
     "croissant": 700
}

# Dictionary with the item and its unitary price
price = {'coffee': 2.00,
         'cake': 5.00,
         'cheese cake': 8.50,
         'croissant': 9.50,}


# Calculate the total worth of the stock in the cafe
total_stock = 0

# Loop through the menu list using items as keys for dictionaries
for item in menu:
    item_value = stock[item] * price[item]
    # Add the item's total value to the overall cafe stock value
    total_stock += item_value

print(f"The total value of the stock is ${total_stock:.2f}.")



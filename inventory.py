# ======= The Beginning of the Class ========
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost =float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"Country: {self.country}, Code: {self.code}, Product: {self.product}, Cost: {self.cost}, Quantity: {self.quantity}"    
    
#  The list will be used to store a list of objects of shoes.
shoe_list = []

# Require Functions
def read_shoes_data():
    """
    Reads data from inventory.txt, handles errors and populates shoe_list.
    """
    shoe_list.clear()

    try:
        with open("inventory.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

            # Skip the header (index 0) and iterate through the data lines
            for i in range(1, len(lines)):
                temp = lines[i].strip().split(",")

                # Verify that the line contains exactly 5 elements
                if len(temp) == 5:
                    country, code, product, cost, quantity = temp
                    shoe_list.append(Shoe(country, code, product, cost, quantity))

        print("\n[Success] Inventory data loaded successfully.")

    except FileNotFoundError:
        print("\n[Error] The File 'inventory.txt' was not found.")
    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")


def write_to_file():
    """
    Writes current shoe_list to inventory.txt including header.
    """
    try:
        with open("inventory.txt", "w", encoding="utf-8") as file:
            file.write("Country,Code,Product,Cost,Quantity\n")
            for shoe in shoe_list:
                file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
    except Exception as e:
        print(f"\n[Error] Could not write to file: {e}")


def capture_shoes():
    country = input("Enter Country: ").strip()
    code = input("Enter Code: ").strip().upper()
    product = input("Enter Product Name: ").strip()

    while True:
        try:
            cost = float(input("Enter Unit Cost: "))
            break
        except ValueError:
            print("Invalid input. Cost must be a number.")


    # Input validation for numerical quantity
    while True:
        try:
            quantity = int(input("Enter Stock Quantity: "))
            break
        except ValueError:
            print("Invalid input. quantity must be a whole number.")

    # Create the new Shoe object object and append 
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)

    # Write the updated list back to the file
    write_to_file()
    print(f"\n[Success] Added: {new_shoe.product} has been saved to the invetory database.")

def view_all():
    """
    Iterates through shoe_list and prints the string representation of 
    all shoes in a clean format.
    """
    if not shoe_list:
        print("\nNo inventory data loaded. Please refresh the data first.")
        return 
    # Print all shoes
    for shoe in shoe_list:
        print(shoe)

    # Find the shoe with the lowest quantity
    lowest_shoe = shoe_list[0]
    for shoe in shoe_list:
        if shoe.quantity < lowest_shoe.quantity:
            lowest_shoe = shoe

    print(f"Product: {lowest_shoe.product} (Code: {lowest_shoe.code}) - Quantity: {lowest_shoe.quantity} units.")

    choice = input("Do you want to re-stock this product? (yes/no): ").strip().lower()
    if choice in ["yes", "y"]:
        while True:
            try:
                additional_qty = int(input(f"Enter quantity to add to '{lowest_shoe.product}': "))
                if additional_qty < 0:
                    print("Please enter a positive value.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a whole number.")

        # Add the stock and save back to file
        lowest_shoe.quantity += additional_qty
        write_to_file()
        print(f"[Success] Stock updated! New quantity: {lowest_shoe.quantity}")
    else:
        print("\nRe-stock operation cancelled.")


def search_shoe():
    if not shoe_list:
        print("\nNo inventory data loaded.")
        return

    search_code = input("\nEnter the shoe code to search: ").strip().upper()
    found = False

    for shoe in shoe_list:
        if shoe.code == search_code:
            print(f"\n-- Product Found ---\n{shoe}")
            found = True
            break

    if not found:
        print(f"\nNo product found matching code '{search_code}'.")


def value_per_item():
    if not shoe_list:
        print("\nNo inventory data loaded.")
        return
    
    print(f"{'PRODUCT':<25} | {'CODE':<12} | ${'TOTAL STOCK VALUE':<18}")

    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        print(f"{shoe.product:<25}|{shoe.code:<12}|${value:<17,.2f}")


def highest_qty():
    """
   Indentifies the shoe with highest stock quantity and prints it
   as a clearance sale advertisement. 
    """      
    if not shoe_list:
        print("\nNo inventory data loaded.")
        return
    
    # Set first shoe as baseline
    highest_shoe = shoe_list[0]

    for shoe in shoe_list:
        if shoe.quantity > highest_shoe.quantity:
            highest_shoe = shoe

    print("\n=================================================")  
    print(f"item: {highest_shoe.product} ({highest_shoe.code})")   
    print(f"Price:${highest_shoe.cost:,.2f} each")
    print(f"Limit: Only {highest_shoe.quantity} units left in stock!")
    print("=======================================================\n")
                
def re_stock():
    if not shoe_list:
        print("\nNo inventory data loaded.")
        return

    lowest_shoe = min(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"\nLowest stock item: {lowest_shoe.product} (Code: {lowest_shoe.code}) - Quantity: {lowest_shoe.quantity} units.")

    choice = input("Do you want to re-stock this product? (yes/no): ").strip().lower()
    if choice in ["yes", "y"]:
        while True:
            try:
                additional_qty = int(input(f"Enter quantity to add to '{lowest_shoe.product}': "))
                if additional_qty < 0:
                    print("Please enter a positive value.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a whole number.")

        lowest_shoe.quantity += additional_qty
        write_to_file()
        print(f"[Success] Stock updated! New quantity: {lowest_shoe.quantity}")
    else:
        print("\nRe-stock operation cancelled.")


def write_to_file():
    """
    Helper function to rewrite current data inside shoe_list
    back to inventory.txt in CSV format.
    """                
    try:
        with open("inventory.txt","w",encoding="utf-8") as file:
            # Rewrite CSV header line
            file.write("Country,Code,Product,Cost,Quantity\n")
            for shoe in shoe_list:
                file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
    except Exception as e:
        print(f"[Error] Failed to save changes to file:{e}")


#============================================
# Main Program Loop
#============================================
def main():
    read_shoes_data()

    while True:
        print("\n=== Inventory Management Menu ===")
        print("1. Read inventory database file")
        print("2. Capture details of a new shoe")
        print("3. View details of all shoes")
        print("4. Re-stock items with lowest quantity")
        print("5. Search for a shoe using its code")
        print("6. Calculate total value for each shoe")
        print("7. Find item with highest quantity (On Sale)")
        print("8. Exit system") 
        print("==============================================")


        choice = input("Enter choice (1-8):").strip()

        if choice == "1":
            read_shoes_data()
        elif choice == "2":
            capture_shoes()
        elif choice == "3":
            view_all()
        elif choice == "4":
            re_stock()  
        elif choice == "5":
            search_shoe()
        elif choice == "6":
            value_per_item()
        elif choice == "7":
            highest_qty()
        elif choice == "8":
            print("\nExiting system... Goodbye!")
            break
        else:
            print("\nInvalid selection. Please choose a valid option(1-8).")

if __name__ == "__main__":
    main()                              



    

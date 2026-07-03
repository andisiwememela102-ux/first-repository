def perform_calculation():
    """
    Prompt the user for two numbers and an operation, then perform the calculation and return the result.
    
    """
    while True: # Loop to allow the user to perform multiple calculations
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            operation = input("Enter the operation (+, -, *, /): ")

            if operation not in ['+', '-', '*', '/']:
                return "Error: Invalid operation. Please enter one of +, -, *, /."

            # Perform the calculation based on the operation
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    return "Error: Division by zero is not allowed."
                result = num1 / num2
            else:
                return "Error: Invalid operation."

            return f"The result of {num1} {operation} {num2} is: {result}"

        except ValueError:
            return "Error: Invalid input. Please enter numeric values."
        
        #Record the calculation in equations.txt
        with open("equations.txt", "a") as file:
            file.write(f"{num1} {operation} {num2} = {result}\n")
            print("Calculation recorded in equations.txt.")
        break  # Exit the loop after a successful calculation

def print_previous_calculations():
        """
        Read and print the previous calculations from equations.txt.
        """
        try:
            with open("equations.txt", "r") as file:
                calculations = file.readlines()
                if calculations:
                    print("Previous calculations:")
                    for calculation in calculations:
                        print(calculation.strip())
                else:
                    print("No previous calculations found.")
        except FileNotFoundError:
            print("No previous calculations found. The file does not exist.")    

def calc_app():
    """
    Main function to run the calculator application.
    """
    while True:
        print("\nWelcome to the Calculator App!")
        print("1. Perform a calculation")
        print("2. View previous calculations")
        print("3. Exit")
        
        choice = input("Please select an option (1, 2, or 3): ")
        
        if choice == '1':
            result = perform_calculation()
            print(result)
        elif choice == '2':
            print_previous_calculations()
        elif choice == '3':
            print("Exiting the Calculator App. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

# Start the app
calc_app()                        
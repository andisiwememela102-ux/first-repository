import math

# Display the menu of finacial calculators
print("Investment - to calculate the amount of interest you'll earn on your investment.")
print("Bond - to calculate the amount you'll have to pay on a home loan.\n")
print("Enter either 'bond' or 'investment' from the menu above to proceed:")

# Get the user's choice
calculator_choice = input().lower().strip()

#--- INVESTMENT PATH ---
if calculator_choice == "investment":
    # Get the necessary inputs for the investment calculator
    principal = float(input("Enter the amount of money your are depositing(p):"))
    interest_rate = float(input("Enter the interest rate(as a percentage):(e.g., 8 instead of 8%):"))
    years = int(input("Enter the number of years you plan to invest:"))
    interest_type = input("Enter 'simple' or 'compound' to choose the type of interest:").lower()

    # Calculate the fractional rate
    r = interest_rate / 100

    # Ask the user for interest type
    if interest_type == "simple":
        # Formula: A = P * (1 + r * t)
        amount = principal * (1 + r * years)
        print(f"Your investment will be worth: R{amount:.2f}")

    elif interest_type == "compound":
        amount = principal * math.pow((1 + r), years)
        print(f"Your investment will be worth: R{amount:.2f}")

    else:
        print("Error: Invalid interest type entered. Enter either 'simple' or 'compound'.")

#--- BOND PATH  ---
elif calculator_choice == "bond":
    # Gather user inputs for bond
    house_value = float(input("Enter the current value of the house: "))
    annual_interest_rate = float(input("Enter the annual interest rate (e.g , 7): "))
    months = int(input("Enter the number of months you plan to take to repay the bond: "))

    # Calculate the monthly repayments
    monthly_rate = (annual_interest_rate / 12) / 100

    repayment = (monthly_rate * house_value) / (1 - math.pow((1 + monthly_rate), -months))

    print(f"Your monthly bond repayment will be: R{repayment:.2f}")

else:
    print("Error: Invalid choice. You must enter either 'bond' or 'investment'.")

  

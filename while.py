# Enter variables to store the sum and count of numbers entered
total_sum = 0
count = 0

# Ask the user to enter a number
while True:
    # Prompt the user for input
    num = input("Enter a number (enter -1 to stop):")

    # Check for the exit condition first
    if num == -1:
        break # This exits the while loop immediately

    # Check for the invalid input condition 
    if num == 0:
        print("Invalid input! Please enter a real number.")
        continue

    # Convert the input to a float
    num = float(num)

    # If the input is not -1 or 0, it is valid.
    # Add itnto the total sum and increment the count.
    count += 1
    total_sum += num

    # Check if any numbers were entered (excluding -1)
    if count > 0:
        # Calculate the average
        average = total_sum / count
        print(f"The average of the numbers entered is:{average}")
    else:
        print("No numbers entered.")    






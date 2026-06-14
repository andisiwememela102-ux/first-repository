# Read the time (in minutes) for each award from the user
swimming_time = float(input("Enter the time (in minutes) for swimming: "))
cycling_time = float(input("Enter the time (in minutes) for cycling: "))
running_time = float(input("Enter the time (in minutes) for running: "))

# Calculate the total time taken for for the triathlon
total_time = swimming_time + cycling_time + running_time

# Display the total time taken
print(f"Total time taken for the triathlon: {total_time} minutes")

#Determine the award based on the total time
if total_time < 100:
    award = "Provincial colours"
elif total_time < 105:
    award = "Provincial half colours"
elif total_time < 110:
    award = "Provincial scroll"
else:
    award = "No award"

# Display the award received
print(f"Award received: {award}")
''' Import the statistics module '''
import statistics


# Ask the user to input 10 floats and store them in a list
float_list = []
print("Please enter 10 number(can be whole numbers or decimals):")

for i in range(10):
    user_input = float(input(f"Enter number{i+1}: "))
    float_list.append(user_input)

print("\n--- Results ---")    

# Find the total of all the numbers and print the result
total_sum = sum(float_list)
print(f"Total sum: {total_sum}")

# Find the index of the maximum value
max_value = max(float_list)
max_index = float_list.index(max_value)
print(f"Index of the maximum value ({max_value}): {max_index}")

# Find the index of the minimum value
min_value = min(float_list)
min_index = float_list.index(min_value)
print(f"Index of the minimum value({min_value}): {min_index}")

# Calculate the average (mean) 
mean_value = statistics.mean(float_list) 
rounded_mean = round(mean_value, 2)
print(f"Average (rounded to 2 decimal places): {rounded_mean}")

# Calculate the median number and Print the results
median_value = statistics.median(float_list)
print(f"Median: {median_value}")
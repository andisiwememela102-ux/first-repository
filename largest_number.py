def largest_number(numbers):
    # Base Case : If the list has only one element left, that element must be the largest
    if len(numbers) ==1:
        return numbers[0]
    

    # Recursive Case: Find the largest number in the rest of the list
    max_of_rest = largest_number(numbers[1:])
    # Compare the first element with the max of the rest and return the larger
    if numbers[0] > max_of_rest:
        return numbers[0]
    else:
        return max_of_rest
    

# Testing the function with the assignment examples 
if  __name__ == "__main__":
    # Test 1
    test_list1 = [1, 4, 5, 3]
    print(f"Largest in {test_list1} => {largest_number(test_list1)}")    

    # Test 2
    test_list2 = [3, 1, 6, 8, 2, 4, 5]
    print(f"Largest in {test_list2} => {largest_number(test_list2)}")
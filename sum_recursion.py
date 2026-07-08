def adding_up_to(numbers, index):
    # Base Case : if the index is 0, we only return the first element
    if index == 0:
        return numbers[0]
    
    # Recursive Case: Add the element at the current index to the sumof all elements before it
    else:
        return numbers[index]  + adding_up_to(numbers, index - 1)    
    

# Testing the function with the assignment examples
if __name__ == "__main__":
    # Test 1
    list1 = [1, 4, 5, 3, 12, 16]
    target_index1 = 4
    print(f"Result 1: {adding_up_to(list1, target_index1)}")  

    # Test 2
    list2 = [4, 3, 1, 5]
    target_index2 = 1
    print(f"Result 2: {adding_up_to(list2, target_index2)}")  
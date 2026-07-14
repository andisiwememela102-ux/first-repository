def merge_sort_by_length(arr):
    """
    Sorts a list of strings by their length in descending order
    (from longest to shortest) using the Merge Sort algorithm.
    
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively sort both halves
        merge_sort_by_length(left_half)
        merge_sort_by_length(right_half)
                             
        # Iterators for traversing the two halves and the main list
        i = j = k = 0

        # Merge the two halves back together
        while i < len(left_half) and j < len(right_half):
            if len(left_half[i]) >= len(right_half[j]):
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
                k += 1


        # Check if any elements were left in the left half 
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1


# Unsorted lists of strings, each containing at least 10 elements:
list_1 = ["apple", "pear", "banana", "pineapple", "orange", "strawberry", "kiwi", "blueberry", "rasberry", "grape"]
list_2 = ["Red", "purple", "pink", "black", "gray", "peach", "blue", "maroon", "velvet", "light blue"]
list_3 = ["toyota", "bmw", "suzuki", "volkwagan", "mercedes benz", "porche", "omoda", "jetour", "audi", "ford"]

all_test_lists = [list_1, list_2, list_3]
    
# Run the test
for idx, string_list in enumerate(all_test_lists, start=1):
    print(f"--- Test List {idx} ---")
    print(f"Original: {string_list}")   

    # Sort the list in place
    merge_sort_by_length(string_list) 

    print(f"Sorted:   {string_list}\n")
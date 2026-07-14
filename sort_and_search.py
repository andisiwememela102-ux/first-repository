# The given unsorted list
num_list = [27, -3, 4, 5, 35, 2, 1, -40, 7, 18, 9, -1, 16, 100]


# Linear search is the most appropriate searching algorith to use
# here because the original list is unsorted. Binary search cannot be 
# perfomed on unsorted data without yielding incorrect results. Since
# the list is very small (14 elements), linear search is highly efficient 
# with a time complexity of 0(n).


def linear_search(arr, target):
    for index, element in enumerate(arr):
        if element == target:
            return index
        return -1 
    
# Search for the number 9 in the unsorted list
linear_search_result = linear_search(num_list, 9)
if linear_search_result != -1: 
    print(f"Linear Search: Found 9 at index {linear_search_result} in the unsorted list.")
else:
    print("Linear Search: 9 was not found in the list.")


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Move element of arr[0..i-1] that are greater than key
        # to one position ahead of their current position
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            arr[j + 1] = key

 # Run insertion Sort on our list
insertion_sort(num_list)

print(f"Sorted List:  {num_list}")
              
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


# Now that the list is sorted, we can implement Binary search to locate
# the number 9.
# Real-World Application:
# Binary search is widely used in systems where data is sorted and needs
# to be queried repeatedly and rapidly. Example include:
# * Looking up a word in a digital dictionary or database indexes.
# * Auto-complete search functions or contact lists in mobile phones.
# * High-frequency trading platforms searching through sorted order books.
# It is preferred because of its incredible 0(log n) logarithmic efficiency.


# Search for the number 9 in the newly sorted list
binary_search_result = binary_search(num_list, 9) 
if binary_search_result != -1:
    print(f"Binary Search : Found 9 at index {binary_search_result} in the sorted list.")
else:
    print("Binary search: 9 was not found in the sorted list.")       



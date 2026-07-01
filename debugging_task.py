# Function to print dictionary values given the keys
def print_values_of(dictionary, keys):
    #FIX: Corrected the variable name from 'k' to 'key' in the print statement


    for key in keys:
        print(dictionary[key]) #Use key instead of k to access the dictionary value

# Print dictionary values from simpson_catch_phrases

simpson_catch_phrases = {"lisa": "BAAAAAART!", 
                         "bart": "Eat My Shorts!", 
                         "marge": "Mmm~mmmmm", 
                         "homer": "d'oh",  #Corrected the string to use double quotes for consistency
                         "maggie": "(Pacifier Suck)"
                         }

# Passed the keys as a list to the function instead of separate arguments
print_values_of(simpson_catch_phrases, ['lisa', 'bart', 'homer']) # Named the list of keys to be passed as a single argument to the function

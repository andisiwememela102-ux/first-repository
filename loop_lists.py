# Define a list of strings of your five favourite movies
fav_movies = ["After", "Forever", "Someone great", "Purple hearts" , "Tallgirl"]

# Loop over the list and print out 
print("--- Simple Loop ---")
for movie in fav_movies:
    print("Movies: " + movie)


print("\n--- Challenge: Enumerated Loop ---")  
for index, movie in enumerate(fav_movies, start=1):
    # Print the index and corresponding movie name
    print(f"Movie {index}: {movie}")
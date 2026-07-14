# 1 & 2 Design the album class
class Album:
    def __init__(self, album_name, number_of_songs, album_artist):
        """ Initialises the instance variables for the Album."""
        self.album_name = album_name
        self.number_of_songs = number_of_songs
        self.album_artist = album_artist

    def __str__(self):
        """Returns a string representation of the Album object."""
        return f"({self.album_name}, {self.album_artist}, {self.number_of_songs})"


# Function to print a list of objects
def print_list(list_name, album_list):
    print(f"\n--- {list_name} ---") 
    for album in album_list:
        print(album)


# Create a new list called album1 and add five album objects 
albums1 = [
        Album("Thriller", 9, "Micheal Jackson"),
        Album("Abbey Road", 17, "The Beatles"),
        Album("Back in Black", 10, "AC/DC"),
        Album("Rumours", 11, "Fleetwood Mac"),
        Album("The Dark Side of the Moon", 10, "Pink Floyd")
]               
print_list("albums1 (initial)", albums1)

# Sort the list according to the number_of_songs and print it out
# Use a lambda function
albums1.sort(key=lambda album: album.number_of_songs)
print_list("albums1 (Sorted by number of songs)", albums1)


# Swap the element at position 1 (index 0)
albums1[0], albums1[1] = albums1[1], albums1[0]
print_list("albums1 (After swapping index 0 and index 1)", albums1)

# Create a new list called albums2
albums2 = []

# Add five Album objects to the albums2 list and print it out
albums2.extend([
    Album("Random Access Memories", 13, "Daft Punk"),
    Album("Discovery", 14, "Daft Punk"),
    Album("After Hours", 14, "The Weeknd"),
    Album("Currents", 13, "Tame Impala"),
    Album("Kid A", 10, "Radiohead"),
])
print_list("albums2 (Initial 5 album)", albums2)

albums2.extend(albums1)

# Add the two specific albums to albums2
albums2.append(Album("Dark Side of the Moon", 9, "Pink Floyd"))
albums2.append(Album("Oops!... I Did It Again", 16, "Britney Spears"))
print_list("albums2 (After copying albums1 and adding specific albums)", albums2)

# Sort the albums in albums2 alphabetically according to the album name
albums2.sort(key=lambda album: album.album_name.lower())
print_list("albums2 (Sorted alphabetically by album name)", albums2)

# Search for the album 'Dark Side of the Moon' in albums2 and print its index
target_album_name = "Dark Side of the Moon"
found_index = -1

# Linear search to find the matching album name
for index, album in enumerate(albums2):
    if album.album_name.lower() == target_album_name.lower():
        found_index = index
        break

print("\n--- Search Result ---")
if found_index != -1:
    print(f"The album '{target_album_name}' was found at index: {found_index}")
    print(f"Details: {albums2[found_index]}")
else:
    print(f"The album '{target_album_name}' was not found.")    
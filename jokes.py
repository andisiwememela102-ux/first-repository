# Import the random module
import random

# Create a list of jokes that include their punchlines
jokes_list = [
    "Why did the computer go to the doctor? Because it had a virus.",
    "Why don't scientists trust atoms? Because they make up everything.",
    "Why did the math book look sad? Because it had too many problems.",
    "Why was the broom late? Because it swept in.",
    "What do you call cheese that isn't yours? Nacho cheese."
]

# Use the random module to display a random joke 
random_joke = random.choice(jokes_list)

print("--- Your Random Joke ---")
print(random_joke)
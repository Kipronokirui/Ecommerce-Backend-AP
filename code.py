import random
import string

def generate_random_string(length):
    characters = string.ascii_uppercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# Example: Generate a random string of length 10
random_string = generate_random_string(10)
print(random_string)
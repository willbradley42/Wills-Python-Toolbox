import random
import string
import secrets

def generate_random_chars(length):
    """
    Algorithm 1: Purely Random Characters.
    Generates a password using a mix of uppercase letters, lowercase letters,
    digits, and special symbols. This is the most common and secure method
    for generating strong, unpredictable passwords.
    """
    if length < 4:
        print("Warning: Length is too short for this algorithm. Returning a 4-character password.")
        length = 4
        
    # Define the character sets to use
    all_chars = string.ascii_letters + string.digits + string.punctuation
    
    # Ensure the password contains at least one of each character type
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]
    
    # Fill the rest of the password length with random characters from the full set
    for _ in range(length - 4):
        password.append(secrets.choice(all_chars))
        
    # Shuffle the list to ensure character positions are random
    random.shuffle(password)
    
    return "".join(password)

def generate_memorable_passphrase(length):
    """
    Algorithm 2: Memorable Passphrase.
    Creates a password by joining randomly selected words. This makes the
    password easier to remember. A random number and separator are added.
    The final length may not exactly match the requested length.
    """
    # A simple word list. For a real application, a larger list is recommended.
    wordlist = [
        "apple", "banana", "galaxy", "mountain", "ocean", "python", "sunshine",
        "guitar", "diamond", "whisper", "velvet", "forest", "river", "castle",
        "dragon", "magic", "wonder", "spirit", "journey", "treasure"
    ]
    separators = ["-", "_", ".", "!", "?", "#"]
    
    # Determine the number of words to use based on average word length
    num_words = max(2, length // 6) 
    
    # Select random words
    selected_words = [secrets.choice(wordlist) for _ in range(num_words)]
    
    # Randomly capitalize some of the words
    for i in range(len(selected_words)):
        if random.choice([True, False]):
            selected_words[i] = selected_words[i].capitalize()
            
    # Join with a random separator and add a random number
    separator = secrets.choice(separators)
    passphrase = separator.join(selected_words) + str(secrets.randbelow(100))
    
    return passphrase

def generate_pronounceable_password(length):
    """
    Algorithm 3: Pronounceable Password (Pattern-based).
    Generates a password by alternating between consonants and vowels,
    making it easier to say out loud. A number is appended for complexity.
    """
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    
    password = ""
    # Start with a consonant or vowel at random
    use_consonant = random.choice([True, False])
    
    for _ in range(length - 2): # Save space for two digits at the end
        if use_consonant:
            password += secrets.choice(consonants)
        else:
            password += secrets.choice(vowels)
        use_consonant = not use_consonant # Alternate
        
    # Add two random digits to the end for complexity
    password += str(secrets.randbelow(100)).zfill(2)
    
    return password

def generate_leetspeak_password(length):
    """
    Algorithm 4: Leetspeak Password.
    This algorithm takes a common word, converts it to "leetspeak" by
    substituting characters (e.g., 'e' -> '3'), and pads it to the
    desired length.
    """
    wordlist = [
        "security", "password", "hacker", "internet", "computer", "system",
        "network", "administrator", "sunshine", "freedom", "awesome"
    ]
    
    substitutions = {
        'a': '@', 'o': '0', 'l': '1', 'i': '!', 's': '$', 'e': '3', 't': '7'
    }
    
    # Choose a base word
    base_word = secrets.choice(wordlist)
    leet_word = ""
    
    # Apply substitutions
    for char in base_word:
        leet_word += substitutions.get(char.lower(), char)
        
    # Pad the password if it's shorter than the desired length
    if len(leet_word) < length:
        padding_length = length - len(leet_word)
        padding_chars = string.digits + string.punctuation
        padding = "".join(secrets.choice(padding_chars) for _ in range(padding_length))
        leet_word += padding
    # Truncate if it's longer
    elif len(leet_word) > length:
        leet_word = leet_word[:length]
        
    return leet_word


def main():
    """Main function to drive the password generator."""
    print("--- Password Generator ---")
    
    while True:
        try:
            length_input = input("Enter desired password length (e.g., 16, or 'q' to quit): ")
            if length_input.lower() == 'q':
                print("Goodbye!")
                break
            
            length = int(length_input)
            if length <= 0:
                print("Please enter a positive number.")
                continue

            # A list containing the four algorithm functions
            algorithms = [
                ("Purely Random", generate_random_chars),
                ("Memorable Passphrase", generate_memorable_passphrase),
                ("Pronounceable", generate_pronounceable_password),
                ("Leetspeak", generate_leetspeak_password),
            ]
            
            # Choose one algorithm at random
            algo_name, chosen_algorithm = secrets.choice(algorithms)
            
            # Generate the password
            password = chosen_algorithm(length)
            
            print("\n" + "="*30)
            print(f"Algorithm Used: {algo_name}")
            print(f"Generated Password: {password}")
            print("="*30 + "\n")

        except ValueError:
            print("Invalid input. Please enter a number for the length.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
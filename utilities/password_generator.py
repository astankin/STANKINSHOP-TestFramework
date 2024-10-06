import random
import string


def generate_random_password(length):
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special_char = random.choice("@$!%*?&")  # Only allow specific special characters
    required_chars = [lowercase, uppercase, digit, special_char]

    all_characters = string.ascii_letters + string.digits + "!@#$%"
    remaining_chars = [random.choice(all_characters) for _ in range(length - 4)]
    password_list = required_chars + remaining_chars
    random.shuffle(password_list)
    return ''.join(password_list)

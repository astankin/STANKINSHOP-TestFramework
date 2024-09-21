import random
import string


def generate_random_email():
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    email_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'example.com', 'yourdomain.com']
    domain = random.choice(email_domains)
    email = f"{username}@{domain}"
    return email

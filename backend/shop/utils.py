import random
import string

def generate_voucher(length=12):
    characters = string.ascii_uppercase + string.digits  # Combining uppercase letters and digits
    return ''.join(random.choice(characters) for _ in range(length))


def obfuscate_card_number(card_number):
    if len(card_number) < 8:
        raise ValueError("Card number too short to obfuscate properly.")
    return f"{card_number[:4]}{'*' * (len(card_number) - 8)}{card_number[-4:]}"
from random import choices
from string import ascii_uppercase, ascii_lowercase, digits


def generate_random(n: int) -> str:
    return "".join(choices(ascii_uppercase + ascii_lowercase + digits, k=n))

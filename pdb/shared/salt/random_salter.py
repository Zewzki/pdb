from pdb.shared.salt.salter import Salter
from random import choices
from string import ascii_uppercase, ascii_lowercase, digits
from pdb.tools.funcs import generate_random


class RandomSalter(Salter):
    def generate_salt(self, n: int) -> str:
        return generate_random(n)

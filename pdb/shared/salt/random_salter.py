from pdb.shared.salt.salter import Salter
from random import choices
from string import ascii_uppercase, ascii_lowercase, digits


class RandomSalter(Salter):
    def generate_salt(self, n: int) -> str:
        return "".join(choices(ascii_uppercase + ascii_lowercase + digits, k=n))

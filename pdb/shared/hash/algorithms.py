from hashlib import pbkdf2_hmac, sha256
from pdb.shared.hash.hash_algorithm import HashAlgorithm
from pdb.shared.hash.supported_hash import SupportedHash


class Sha256(HashAlgorithm):
    @property
    def name(self) -> str:
        return SupportedHash.SHA256.value

    def hash(self, input: str, salt: str) -> bytes:
        return sha256((input + salt).encode("utf-8")).digest()


class PBKDF2(HashAlgorithm):
    @property
    def name(self) -> str:
        return SupportedHash.PBKDF2.value

    def hash(self, input: str, salt: str) -> bytes:
        return pbkdf2_hmac(self.name, input, salt)

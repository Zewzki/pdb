from pdb.shared.hash.algorithms import PBKDF2, Sha256
from pdb.shared.hash.hash_algorithm import HashAlgorithm
from pdb.shared.hash.supported_hash import SupportedHash


class HasherFactory:
    @classmethod
    def create_hasher(cls, hash_type: SupportedHash) -> HashAlgorithm:
        match hash_type:
            case SupportedHash.SHA256:
                return Sha256()
            case SupportedHash.PBKDF2:
                return PBKDF2()

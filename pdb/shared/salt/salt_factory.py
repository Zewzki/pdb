from pdb.shared.salt.random_salter import RandomSalter
from pdb.shared.salt.salter import Salter
from pdb.shared.salt.supported_salter import SupportedSalter


class SaltFactory:
    @classmethod
    def create_salter(cls, salter_type: SupportedSalter) -> Salter:
        match salter_type:
            case SupportedSalter.RANDOM:
                return RandomSalter()

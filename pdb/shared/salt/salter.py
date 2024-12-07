from abc import ABC, abstractmethod


class Salter(ABC):
    @abstractmethod
    def generate_salt(self, n: int) -> str:
        pass

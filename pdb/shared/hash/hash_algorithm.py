from abc import ABC, abstractmethod


class HashAlgorithm(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def hash(self, input: str, salt: str) -> str:
        pass

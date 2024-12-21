from abc import ABC, abstractmethod
from typing import Any


class RequestExtractor(ABC):
    @abstractmethod
    def request_as_dict(self, request: Any) -> dict[str, Any]:
        pass

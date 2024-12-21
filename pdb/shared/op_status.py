from dataclasses import dataclass
from typing import Any


@dataclass
class OpStatus:
    status: bool
    content: Any

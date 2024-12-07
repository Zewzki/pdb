from dataclasses import dataclass


@dataclass
class OpStatus:
    status: bool
    msg: str

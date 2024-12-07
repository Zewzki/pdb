from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    port: int | None = None
    db: str | None = None
    user: str | None = None
    password: str | None = None
    options: dict[str, str] | None = None
    debug: bool = False

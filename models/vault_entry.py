from dataclasses import dataclass

@dataclass
class VaultEntry:
    id: int
    title: str
    username: str
    password: str
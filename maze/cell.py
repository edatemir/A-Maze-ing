
from dataclasses import dataclass, field

def walls() -> dict[str, bool]:      #mutable default calis
    walls = {
        "N": True,
        "E": True,
        "S": True,
        "W": True,
    }
    return walls


@dataclass
class Cell:
    x: int
    y: int
    visited: bool = False
    blocked: bool = False
    walls: dict[str, bool] = field(default_factory=walls)


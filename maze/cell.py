
from dataclasses import dataclass, field


def walls() -> dict[str, bool]:
    """Default value for Cell.walls: all four sides start closed."""
    walls = {
        "N": True,
        "E": True,
        "S": True,
        "W": True,
    }
    return walls


@dataclass
class Cell:
    """A single maze cell: its position, visited/blocked state, and walls on
    each side."""
    x: int
    y: int
    visited: bool = False
    blocked: bool = False
    walls: dict[str, bool] = field(default_factory=walls)

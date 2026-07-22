
from maze.exceptions import (
    ConfigFileError,
    ConfigSyntaxError,
    ConfigMissingKeyError,
    ConfigValueError,
    ConfigValidationError,
    ) 

from dataclasses import dataclass

@dataclass
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def parse_config(path: str) -> Config:
    lines = read_file(path)
    raw_data = parse_line(lines)
    key(raw_data)
    return build_config(raw_data)


def read_file(path: str) -> list[str]:
    try:
        with open(path) as file: #encoding eklenmeli mi
            lines = file.read().splitlines()
        return lines
    except FileNotFoundError as error:
        raise ConfigFileError(f"Config file '{path}' not found.") from error
    except PermissionError as error:
        raise ConfigFileError(f"Unable to read '{path}' file.") from error
    

def parse_line(lines: list[str]) -> dict[str, str]:
    raw_data = {}
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            continue
        if line.count("=") != 1:
            raise ConfigSyntaxError(f"Syntax Error")
        key, value = line.split("=")
        key = key.strip().upper()
        value = value.strip()
        if key == "":
            raise ConfigSyntaxError(f"Syntax Error")
        if key in raw_data:
            raise ConfigSyntaxError(f"Syntax Error")
        if value == "":
            raise ConfigSyntaxError(f"Syntax Error")
        raw_data[key] = value
    return raw_data


def key(raw_data: dict[str, str]) -> None:
    required_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    ]
    allowed_keys = set(required_keys) | {"SEED"}
    for required_key in required_keys:
        if required_key not in raw_data:
            raise ConfigMissingKeyError(f"{required_key} config key missing")
    for config_key in raw_data:
        if config_key not in allowed_keys:
            raise ConfigSyntaxError(f"Unknown config key '{config_key}'")


def build_config(raw_data: dict[str, str]) -> Config:
    try:
        width = int(raw_data["WIDTH"])
    except ValueError:
        raise ConfigValueError(f"Width must be a number")
    if width <= 0:
        raise ConfigValidationError(f"Width must be greater than 0")
    
    try:
        height = int(raw_data["HEIGHT"])
    except ValueError:
        raise ConfigValueError(f"Height must be a number")
    if height <= 0:
        raise ConfigValidationError(f"Height must be greater than 0")
    
    parts = raw_data["ENTRY"].split(",")
    if len(parts) != 2:
        raise ConfigSyntaxError(f"Entry must be in x,y format")
    try:
        x = int(parts[0])
    except ValueError:
        raise ConfigValueError(f"Entry x must be a number")
    try:
        y = int(parts[1])
    except ValueError:
        raise ConfigValueError(f"Entry y must be a number")
    entry = (x,y)

    coordinates = raw_data["EXIT"].split(",")
    if len(coordinates) != 2:
        raise ConfigSyntaxError(f"Exit must be in x,y format")
    try:
        x_exit = int(coordinates[0])
    except ValueError:
        raise ConfigValueError(f"Exit x must be a number")
    try:
        y_exit = int(coordinates[1])
    except ValueError:
        raise ConfigValueError(f"Exit y must be a number")
    exit = (x_exit,y_exit)

    output_file = raw_data["OUTPUT_FILE"]

    perfect_value = raw_data["PERFECT"].lower()
    if perfect_value == "true":
        perfect = True
    elif perfect_value == "false":
        perfect = False
    else:
        raise ConfigValueError(f"Perfect must be bool")
    
    if "SEED" in raw_data:
        try:
            seed = int(raw_data["SEED"])
        except ValueError:
            raise ConfigValueError(f"Seed must be an integer")
    else:
        seed = None

    if x < 0 or x >= width:
        raise ConfigValidationError(f"Entry x is outside the maze boundaries.")
    if y < 0 or y >= height:
        raise ConfigValidationError(f"Entry y is outside the maze boundaries.")
    
    if x_exit < 0 or x_exit >= width:
        raise ConfigValidationError(f"Exit x is outside the maze boundaries.")
    if y_exit < 0 or y_exit >= height:
        raise ConfigValidationError(f"Exit y is outside the maze boundaries.")
    
    if entry == exit:
        raise ConfigValidationError(f"Entry and Exit cannot be the same position")
    
    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
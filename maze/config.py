
from maze.exceptions import (
    ConfigFileError,
    ConfigSyntaxError,
    ConfigMissingKeyError,
    ConfigValueError,
    ConfigValidationError,
    ) 

from dataclasses import dataclass

@dataclass #frozen=True config yapılmalı mı
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
        if "=" not in line:
            raise ConfigSyntaxError(f"Syntax Error")
        if line.count("=") != 1:
            raise ConfigSyntaxError(f"Syntax Error")
        key, value = line.split("=")
        key = key.strip().upper()
        value = value.strip()
        if key == "":
            raise ConfigSyntaxError(f"Syntax Error")
        if value == "":
            raise ConfigSyntaxError(f"Syntax Error")
        raw_data[key] = value
    return raw_data

def key(raw_data: dict[str, str]) -> None:


def build_config(raw_data: dict[str, str]) -> Config:

class ConfigError(Exception):
    """Base class for all config-file related errors."""
    pass

class ConfigFileError(ConfigError):
    """Raised when the config file cannot be found or read."""
    pass

class ConfigSyntaxError(ConfigError):
    """Raised when a config line doesn't follow the KEY=VALUE format."""
    pass

class ConfigMissingKeyError(ConfigError):
    """Raised when a required config key is missing."""
    pass

class ConfigValueError(ConfigError):
     """Raised when a config value has the wrong type (not a number, not a bool, etc.)."""
    pass

class ConfigValidationError(ConfigError):
    """Raised when config values are well-typed but logically invalid (e.g. entry out of bounds)."""
    pass

class MazeError(Exception):
    """Base class for all maze-generation errors."""
    pass

class MazeGenerationError(MazeError):
     """Raised when the maze cannot be generated as required."""
    pass

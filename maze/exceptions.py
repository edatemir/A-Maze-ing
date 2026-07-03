
class ConfigError(Exception):
    pass

class ConfigFileError(ConfigError):
    pass

class ConfigSyntaxError(ConfigError):
    pass

class ConfigMissingKeyError(ConfigError):
    pass

class ConfigValueError(ConfigError):
    pass

class ConfigValidationError(ConfigError):
    pass
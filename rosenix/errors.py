class RosenixError(Exception):
    pass

class ConfigurationError(RosenixError):
    pass

class ProviderError(RosenixError):
    pass

class ToolError(RosenixError):
    pass

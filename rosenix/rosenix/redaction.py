DEFAULT_SENSITIVE_KEYS = {"password", "token", "secret", "api_key"}


def redact_mapping(values, replacement="***", sensitive_keys=None):
    keys = {str(key).lower() for key in (sensitive_keys or DEFAULT_SENSITIVE_KEYS)}
    return {key: replacement if str(key).lower() in keys else value for key, value in values.items()}

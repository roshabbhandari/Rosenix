SENSITIVE_KEYS = {"api_key", "token", "password", "secret", "authorization"}

def redact_mapping(values: dict) -> dict:
    return {
        key: "[REDACTED]" if key.lower() in SENSITIVE_KEYS else value
        for key, value in values.items()
    }

def redact_text(value: str, secrets: list[str]) -> str:
    for secret in secrets:
        if secret:
            value = value.replace(secret, "[REDACTED]")
    return value

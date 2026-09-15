from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    value: object = None
    error: Exception = None

    @property
    def ok(self):
        return self.error is None

    @classmethod
    def success(cls, value=None):
        return cls(value=value)

    @classmethod
    def failure(cls, error):
        if not isinstance(error, Exception):
            raise TypeError("error must be an Exception")
        return cls(error=error)

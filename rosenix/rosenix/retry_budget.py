class RetryBudget:
    def __init__(self, limit):
        if limit < 0:
            raise ValueError("limit must be non-negative")
        self.limit = limit
        self.used = 0

    @property
    def remaining(self):
        return self.limit - self.used

    def consume(self, amount=1):
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if amount > self.remaining:
            return False
        self.used += amount
        return True

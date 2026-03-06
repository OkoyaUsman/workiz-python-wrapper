"""Custom exceptions for the Workiz API wrapper."""


class WorkizError(Exception):
    """Base exception for all Workiz API errors."""

    pass


class WorkizAPIError(WorkizError):
    """Exception raised when the API returns an error response."""

    def __init__(self, message: str, code: int = None, details: list = None):
        self.message = message
        self.code = code
        self.details = details or []
        super().__init__(self.message)

    def __str__(self):
        if self.code:
            return f"Workiz API Error {self.code}: {self.message}"
        return f"Workiz API Error: {self.message}"


class WorkizAuthenticationError(WorkizAPIError):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Invalid API credentials"):
        super().__init__(message, code=401)
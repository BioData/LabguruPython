# labguru/exceptions.py
class LabguruError(Exception):
    """Base class for all Labguru SDK errors."""


class LabguruAPIError(LabguruError):
    """Raised when the Labguru API returns a 4xx/5xx response."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Labguru API error {status_code}: {message}")

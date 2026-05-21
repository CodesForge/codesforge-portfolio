class DomainError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class ValidationError(DomainError):
    def __init__(self, message: str):
        super().__init__(message)
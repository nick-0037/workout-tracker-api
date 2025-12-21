from fastapi import status

class AppException(Exception):
    def __init__(self, message: str, code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code 
        super().__init__(message)
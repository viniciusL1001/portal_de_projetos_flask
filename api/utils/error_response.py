class ErrorResponse(Exception):
    def __init__(self, httpCode, message, error=None):
        super().__init__(message)
        self.httpCode = httpCode
        self.error = error

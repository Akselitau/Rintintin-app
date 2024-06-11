class CustomError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class BadRequestError(CustomError):
    def __init__(self, message="Bad request"):
        super().__init__(message, 400)


class NotFoundError(CustomError):
    def __init__(self, message="Not found"):
        super().__init__(message, 404)


class UnauthorizedError(CustomError):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)


class InternalServerError(CustomError):
    def __init__(self, message="Internal server error"):
        super().__init__(message, 500)

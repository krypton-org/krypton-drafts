class KryptonException(Exception):
    api_type = ""
    mapping = {}

    def __new__(cls, error):
        subclass = cls.mapping[error["type"]]
        return super().__new__(subclass)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.mapping[cls.api_type] = cls

    def __init__(self, error):
        super().__init__(error["message"])


class GraphQLError(KryptonException):
    api_type = "GraphQLError"


class EmailAlreadyExistsError(KryptonException):
    api_type = "EmailAlreadyExistsError"

class WrongPasswordError(KryptonException):
    api_type = "WrongPasswordError"


class UpdatePasswordTooLateError(KryptonException):
    api_type = "UpdatePasswordTooLateError"


class EmailNotSentError(KryptonException):
    api_type = "EmailNotSentError"


class UserNotFoundError(KryptonException):
    api_type = "UserNotFoundError"


class UnauthorizedError(KryptonException):
    api_type = "UnauthorizedError"


class EmailAlreadyConfirmedError(KryptonException):
    api_type = "EmailAlreadyConfirmedError"


class UserValidationError(KryptonException):
    api_type = "UserValidationError"


class AlreadyLoggedInError(KryptonException):
    api_type = "AlreadyLoggedInError"

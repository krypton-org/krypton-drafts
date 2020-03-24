from typing import Dict


class KryptonException(Exception):
    api_type = ""

    def __init__(self, error: Dict):
        super().__init__(error["message"])


class GraphQLError(KryptonException):
    api_type = "GraphQLError"


class EmailAlreadyExistsError(KryptonException):
    api_type = "EmailAlreadyExistsError"


class UsernameAlreadyExistsError(KryptonException):
    api_type = "UsernameAlreadyExistsError"


class WrongPasswordError(KryptonException):
    api_type = "WrongPasswordError"


class UpdatePasswordTooLateError(KryptonException):
    api_type = "UpdatePasswordTooLateError"


class EmailNotSentError(KryptonException):
    api_type = "EmailNotSentError"


class UserNotFound(KryptonException):
    api_type = "UserNotFound"


class EmailAlreadyConfirmedError(KryptonException):
    api_type = "EmailAlreadyConfirmedError"


class UserValidationError(KryptonException):
    api_type = "UserValidationError"


class AlreadyLoggedInError(KryptonException):
    api_type = "AlreadyLoggedInError"


exceptions = [
    GraphQLError,
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
    WrongPasswordError,
    UpdatePasswordTooLateError,
    EmailNotSentError,
    UserNotFound,
    EmailAlreadyConfirmedError,
    UserValidationError,
    AlreadyLoggedInError,
]

ExceptionMapping = {exc.api_type: exc for exc in exceptions}

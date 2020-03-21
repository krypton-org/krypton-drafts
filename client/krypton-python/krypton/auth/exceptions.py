class KryptonAuthException(Exception):
    api_type = None
    mapping = {}

    def __new__(cls, error):
        subclass = cls.mapping[error["type"]]
        return super().__new__(subclass)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.mapping[cls.api_type] = cls

    def __init__(self, error):
        super().__init__(error["message"])


class GraphQLError(KryptonAuthException):
    api_type = "GraphQLError"


class EmailAlreadyExistsError(KryptonAuthException):
    api_type = "EmailAlreadyExistsError"


class UsernameAlreadyExistsError(KryptonAuthException):
    api_type = "UsernameAlreadyExistsError"


class WrongPasswordError(KryptonAuthException):
    api_type = "WrongPasswordError"


class UserNotFound(KryptonAuthException):
    api_type = "UserNotFound"

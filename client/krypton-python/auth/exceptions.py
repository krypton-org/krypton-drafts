class GraphQLAuthException(Exception):
    mapping = {}

    def __new__(cls, error):
        subclass = cls.mapping[error["type"]]
        return super().__new__(subclass)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.mapping[cls.api_type] = cls

    def __init__(self, error):
        super().__init__(error["message"])


class GraphQLError(GraphQLAuthException):
    api_type = "GraphQLError"

class EmailAlreadyExistsError(GraphQLAuthException):
    api_type = "EmailAlreadyExistsError"

class UsernameAlreadyExistsError(GraphQLAuthException):
    api_type = "UsernameAlreadyExistsError"

class WrongPasswordError(GraphQLAuthException):
    api_type = "WrongPasswordError"

class UserNotFound(GraphQLAuthException):
    api_type = "UserNotFound"

# TODO

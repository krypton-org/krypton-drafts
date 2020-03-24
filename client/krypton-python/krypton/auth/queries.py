from typing import Any, Dict


class Query:
    query = ""
    "GraphQL query"

    variables: Dict = {}
    "GraphQL variables"

    def __init__(self, **variables: Any):
        self.variables = variables

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.variables})"

    def to_dict(self) -> Dict:
        return {"query": self.query, "variables": self.variables}


class RefreshQuery(Query):
    query = "mutation { refreshToken { token } }"


class RegisterQuery(Query):
    query = """
        mutation register($fields: UserRegisterInput!) {
            register(fields: $fields) {
                notifications { type }
            }
        }
    """


class LoginQuery(Query):
    query = """
            mutation login($login: String!, $password: String!) {
                login(login: $login, password: $password) {
                    token
                }
            }
        """


class UpdateQuery(Query):
    query = """
            mutation updateMe($fields: UserUpdateInput!) {
                updateMe(fields: $fields) {
                    notifications { type }
                }
            }
        """


class DeleteQuery(Query):
    query = """
            mutation deleteMe($password: String!) {
                deleteMe(password: $password) {
                    notifications { type }
                }
            }
        """

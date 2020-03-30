class Query:
    query = ""
    variables = {}

    def __init__(self, **variables):
        self.variables = variables

    def __repr__(self):
        return f"{self.__class__.__name__}({self.variables})"

    def to_dict(self):
        return {"query": self.query, "variables": self.variables}


class RefreshQuery(Query):
    query = "mutation { refreshToken { token } }"


class RegisterQuery(Query):
    query = """
        mutation register($fields: UserRegisterInput!) {
            register(fields: $fields)
        }
    """


class LoginQuery(Query):
    query = """
            mutation login($email: String!, $password: String!) {
                login(email: $email, password: $password) {
                    token
                }
            }
        """


class UpdateQuery(Query):
    query = """
            mutation updateMe($fields: UserUpdateInput!) {
                updateMe(fields: $fields) {
                    token
                }
            }
        """


class DeleteQuery(Query):
    query = """
            mutation deleteMe($password: String!) {
                deleteMe(password: $password)
            }
        """

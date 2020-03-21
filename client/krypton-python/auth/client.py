import requests
from auth.exceptions import GraphQLAuthException
from auth.graphql import Argument, Field, Mutation, Operation, Query

# https://stackoverflow.com/a/14620633
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


# TODO: Client serialization (token, cookies)
# TODO: GraphQLAuthState object ?


class BaseGraphQLAuthClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.session = requests.Session()

    def post(self, **kwargs) -> dict:
        res = self.session.post(self.endpoint, **kwargs)
        print(res.status_code)
        res = res.json()
        print(res)
        return res.get("data"), res.get("errors")

    def query(self, q: Operation) -> AttrDict:
        data, errors = self.post(json={"query": str(q)})

        if errors:
            raise GraphQLAuthException(errors[0])

        # Save token on login/refresh
        # NOTE: The refresh token is stored in the session cookies.
        token = (data.get("login", {}) or data.get("refreshToken", {})).get("token")
        self.session.headers.update({"Authorization": f"Bearer {token}"})

        return AttrDict(data)


class GraphQLAuthClient(BaseGraphQLAuthClient):
    def public_key(self) -> str:
        return self.query(Query(Field("publicKey"))).publicKey

    # TODO: Return type, strict mypy configuration
    # TODO: Type for notifications ?
    def register(self, username: str, email: str, password: str, **kwargs):
        user = {"username": username, "email": email, "password": password, **kwargs}
        notifications = Field("notifications", fields=[Field("type"), Field("message")])
        return self.query(
            Mutation(Field("register", Argument("fields", user), notifications))
        ).register

    def login(self, login: str, password: str):
        field = Field(
            "login",
            (Argument("login", login), Argument("password", password)),
            (Field("token"), Field("expiryDate"), Field("user")),
        )
        return self.query(Mutation(field)).login

    def delete(self, password: str):
        notifications = Field("notifications", fields=[Field("type"), Field("message")])
        field = Field("deleteMe", Argument("password", password), notifications)
        return self.query(Mutation(field)).deleteMe

import jwt
import requests

from .exceptions import KryptonException, UnauthorizedError
from .queries import DeleteQuery, LoginQuery, RefreshQuery, RegisterQuery, UpdateQuery


class UserToken:
    def __init__(self, user, token):
        self.user = user
        self.token = token

    @property
    def header(self):
        return f"Bearer {self.token}"

    @classmethod
    def from_token(cls, token):
        user = jwt.decode(token, verify=False)
        return cls(user, token)


class KryptonAuthClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.session = requests.Session()
        self.token = None

    def __post(self, **kwargs):
        if self.token:
            self.session.headers.update({"Authorization": self.token.header})
        res = self.session.post(self.endpoint, **kwargs)
        return dict(res.json())

    def __query(self, q):
        res = self.__post(json=q.to_dict())

        if "errors" in res:
            error = res["errors"][0]
            raise KryptonException(error)

        # We *must* have data if there is no errors.
        data = res["data"]

        token = (
            data.get("login", {})
            or data.get("refreshToken", {})
            or data.get("updateMe", {})
        ).get("token")

        if token:
            self.token = UserToken.from_token(token)

        return data

    def query(self, q):
        try:
            result = self.__query(q)
        except UnauthorizedError:
            self.refresh()
            result = self.__query(q)
        return result

    def refresh(self):
        self.__query(RefreshQuery())

    def register(self, email, password, **kwargs):
        fields = {"email": email, "password": password, **kwargs}
        self.query(RegisterQuery(fields=fields))

    def login(self, email, password):
        self.query(LoginQuery(email=email, password=password))

    def update(self, **kwargs):
        self.query(UpdateQuery(fields=kwargs))

    def delete(self, password):
        self.query(DeleteQuery(password=password))

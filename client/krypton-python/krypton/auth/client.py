from dataclasses import dataclass

import jwt
import requests

from .exceptions import KryptonException, UnauthorizedError
from .queries import DeleteQuery, LoginQuery, RefreshQuery, RegisterQuery, UpdateQuery


@dataclass(frozen=True)
class UserToken:
    user: dict
    token: str

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

    def post(self, **kwargs):
        if self.token:
            self.session.headers.update({"Authorization": self.token.header})
        res = self.session.post(self.endpoint, **kwargs)
        return res.json()

    def query(self, q, try_refresh=True):
        res = self.post(json=q.to_dict())

        if "errors" in res:
            err = KryptonException(res["errors"][0])
            if isinstance(err, UnauthorizedError) and try_refresh:
                self.query(RefreshQuery(), try_refresh=False)
                return self.query(q, try_refresh=False)
            raise err

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

    def register(self, email, password, **kwargs):
        fields = {"email": email, "password": password, **kwargs}
        self.query(RegisterQuery(fields=fields))

    def login(self, email, password):
        self.query(LoginQuery(email=email, password=password))

    def update(self, **kwargs):
        self.query(UpdateQuery(fields=kwargs))

    def delete(self, password):
        self.query(DeleteQuery(password=password))

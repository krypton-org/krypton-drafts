from typing import Any, Dict, Optional, Tuple

import jwt
import requests

from .exceptions import ExceptionMapping, UnauthorizedError
from .queries import (
    DeleteQuery,
    LoginQuery,
    Query,
    RefreshQuery,
    RegisterQuery,
    UpdateQuery,
)


class UserToken:
    def __init__(self, user, token):
        self.user = user
        self.token = token

    @classmethod
    def from_token(cls, token):
        user = jwt.decode(token, verify=False)
        return cls(user, token)


class KryptonAuthClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.session = requests.Session()
        self.token: Optional[UserToken] = None

    def __post(self, q: Query) -> Dict:
        res = self.session.post(self.endpoint, json=q.to_dict()).json()
        if "errors" in res:
            error = res["errors"][0]
            raise ExceptionMapping[error["type"]](error)
        return dict(res["data"])

    def __query(self, q: Query) -> Dict:
        data = self.__post(q)

        token = (
            data.get("login", {})
            or data.get("refreshToken", {})
            or data.get("updateMe", {})
        ).get("token")

        if token:
            self.token = UserToken.from_token(token)
            self.session.headers.update({"Authorization": f"Bearer {token}"})

        return data

    def query(self, q: Query) -> Dict:
        try:
            result = self.__query(q)
        except UnauthorizedError:
            self.refresh()
            result = self.__query(q)
        return result

    def refresh(self) -> None:
        self.query(RefreshQuery())

    def register(self, username: str, email: str, password: str, **kwargs: Any):
        fields = {"username": username, "email": email, "password": password, **kwargs}
        self.query(RegisterQuery(fields=fields))

    def login(self, login: str, password: str):
        self.query(LoginQuery(login=login, password=password))

    def update(self, **kwargs: Any):
        self.query(UpdateQuery(fields=kwargs))

    def delete(self, password: str):
        self.query(DeleteQuery(password=password))

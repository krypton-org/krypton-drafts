from typing import Any, Dict, Optional, Tuple

import jwt
import requests

from .exceptions import ExceptionMapping, UserNotFound
from .queries import (
    DeleteQuery,
    LoginQuery,
    Query,
    RefreshQuery,
    RegisterQuery,
    UpdateQuery,
)

# TODO: docstrings
# TODO: Queries not needed anymore?


class BaseKryptonAuthClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.session = requests.Session()
        self.user: Optional[Dict] = None
        self.token: Optional[str] = None

    def __post(self, q: Query) -> Dict:
        res = self.session.post(self.endpoint, json=q.to_dict()).json()
        if "errors" in res:
            error = res["errors"][0]
            raise ExceptionMapping[error["type"]](error)
        return dict(res["data"])

    def __query(self, q: Query) -> Dict:
        data = self.__post(q)

        # TODO: Also look into "updateMe" for token
        token = (data.get("login", {}) or data.get("refreshToken", {})).get("token")
        if token:
            self.user = jwt.decode(token, verify=False)
            self.token = token
            self.session.headers.update({"Authorization": f"Bearer {token}"})

        return data

    def query(self, q: Query) -> Dict:
        try:
            result = self.__query(q)
        except:  # Unauthorized:
            # Authenticated queries: refresh token and retry.
            self.refresh()
            result = self.__query(q)
        return result

    def refresh(self) -> None:
        self.query(RefreshQuery())


class KryptonAuthClient(BaseKryptonAuthClient):
    def register(self, username: str, email: str, password: str, **kwargs: Any):
        fields = {"username": username, "email": email, "password": password, **kwargs}
        self.query(RegisterQuery(fields=fields))

    def login(self, login: str, password: str):
        self.query(LoginQuery(login=login, password=password))

    def update(self, **kwargs: Any):
        self.query(UpdateQuery(fields=kwargs))

    def delete(self, password: str):
        self.query(DeleteQuery(password=password))

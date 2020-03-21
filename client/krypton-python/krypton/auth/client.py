import logging
from typing import Dict

import jwt
import requests

from .exceptions import KryptonAuthException, UserNotFound
from .graphql import Argument as A
from .graphql import Field as F
from .graphql import Mutation as M
from .graphql import Operation
from .graphql import Query as Q


class BaseKryptonAuthClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    def post(self, **kwargs) -> dict:
        res = self.session.post(self.endpoint, **kwargs)
        res = res.json()
        return res.get("data"), res.get("errors")

    def query(self, q: Operation) -> Dict:
        data, error = self.post(json={"query": str(q)})

        if error:
            error = KryptonAuthException(error[0])

        if isinstance(error, UserNotFound):
            self.logger.debug("Invalid token, refreshing...")
            self.refresh()
            return self.query(q)

        # Save token on login/refresh
        # NOTE: The refresh token is stored in the session cookies.
        token = (data.get("login", {}) or data.get("refreshToken", {})).get("token")
        self.session.headers.update({"Authorization": f"Bearer {token}"})

        return data

    def refresh(self):
        field = F("refreshToken", fields=F("token"))
        return self.query(M(field))


class KryptonAuthClient(BaseKryptonAuthClient):
    def register(self, username: str, email: str, password: str, **kwargs):
        notifications = F("notifications", fields=[F("type"), F("message")])
        user = {"username": username, "email": email, "password": password, **kwargs}
        self.query(M(F("register", A("fields", user), notifications)))

    def login(self, login: str, password: str):
        field = F("login", (A("login", login), A("password", password)), F("token"))
        res = self.query(M(field))
        return jwt.decode(res["login"]["token"], verify=False)

    def delete(self, password: str):
        notifications = F("notifications", fields=[F("type"), F("message")])
        field = F("deleteMe", A("password", password), notifications)
        self.query(M(field))

    def update(self, **kwargs):
        notifications = F("notifications", fields=[F("type"), F("message")])
        field = F("updateMe", A("fields", kwargs), notifications)
        self.query(M(field))
        res = self.refresh()
        return jwt.decode(res["refreshToken"]["token"], verify=False)

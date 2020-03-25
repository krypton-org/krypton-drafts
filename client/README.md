# Krypton Client Specification

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

There is two types of clients:
- *User clients*: they provide an API to manage a single user session in a client application. In the future, they will also provide UI views to ease the integration into applications.
- *Middlewares*: they integrate with server frameworks (Django, Express, etc.) to verify token signatures, and inject the decoded token in the request.

As far as possible, clients must follow the idioms and conventions of the target platform/language.

## User Clients

### State

User clients are typically stateful since they need to store the user token and the refresh token.
Clients must be thread-safe, such that a client instantiated in one thread, can be safely re-used in another thread.

### API

User clients must implement the following **public** API:

#### Unauthenticated requests

- `emailAvailable(email: str) -> boolean`
- `usernameAvailable(username: str) -> boolean`
- `registerWithEmail(email: str, password: str, **fields) -> (boolean, Optional[Error])`
- `registerWithUsernameAndEmail(username: str, email: str, password: str, **fields) -> (boolean, Optional[Error])`
- `login(login: str, password: str) -> (Optional[Dict], Optional[Error])`
- `resetPassword(email: str) -> boolean`
- `userOne(**fields) -> (Optional[Dict], Optional[Error])`
- `userById(id: str) -> (Optional[Dict], Optional[Error])`
- `userByIds(ids: List[str]) -> (List[Dict], Optional[Error])`
- `userMany(sort: enum[sorts], skip: integer, limit: integer, **filters) -> (List[Dict], Optional[Error])`
- `userMany(**filters) -> (List[Dict], Optional[Error])`
- `userMany(sort: enum[sorts],**filters) -> (List[Dict], Optional[Error])`
- `userCount(**filters) -> integer`
- `userPagination(page: int, perPage: int, sort: enum[sorts], **filters) -> (Optional[Dict] , Optional[Error])`

The choice between `registerWithEmail` and `registerWithUsernameAndEmail` functions depends on the option `hasUsername: boolean` set on Krypton Authentication (server side).
In the `login` and `refreshToken` functions, the user is decoded from the token returned by the server.
In the `user...` functions, all public fields are requested.**

#### Authenticated requests

- `update(**fields) -> (Optional[Dict], Optional[Error])`
- `delete(password: str) -> (Optional[Error])`
- `changePassword(oldPassword: str, newPassord: str) -> Optional[Error]`
- `sendVerificationEmail() -> boolean`

#### Other requests

The following functions may be implemented in the public or private API of the client.
They are typically not used directly by the user.

- `publicKey() -> str`
- `refreshToken() -> (Optional[Dict], Optional[Error])`

### Send authenticated requests to other URLs

User clients must provide a way to make authenticated requests to any other URLs not part of the Krypton Authentication API.
It is done by setting in the `Authorization` HTTP header the following value `Bearer {token}`, `{token}` being the user token.
This can be done in two ways.

#### Return an updated user token

User clients must provide a function returning the user token and its expiryDate. The user token must not be expired nor close to be expired (less than 2 minuts).
- `getToken() -> (token, expiryDate)`

**Note**: the refresh token is not exposed as it is internal to Krypton Authentication.

#### Provide an API to make authenticated requests
User clients should provide an API to make authenticated HTTP requests including automatically the user token in the `Authorization` header. It should also allow to customize requests: [HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods), [target](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages), [version](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages), [headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) (other than the Authorization header) and [body](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages).

### UI Views

TBD

### Error Handling

#### Exceptions

If permitted by the language, errors must be raised as typed exceptions, such that the client can be used as follow:

```python
client = KryptonClient()
try:
  client.register(...)
except UsernameAlreadyExistsError:
  print('Username already exists...')
```

Error messages and their internationalization must be provided by the client.

#### Token Invalidation

The user token (JWT) can be invalidated at any time, either because it expired, or because it was deleted from the server.

1. For every [authenticated request](#Authenticated-requests) the client must check whether or not an error was returned from the server.
2. If a `UnauthorizedError` is returned, it must try to obtain a new token using the `refreshToken` mutation.
3. If a new token is obtained, then it must perform the request again, and return the result to the user.
4. Otherwise the user is considered as logged-out, and a `UnauthorizedError` exception is raised.

<img src="client.png" height=400px />


## Middlewares

Middlewares must integrate with server frameworks (Django, Express, etc.) in their standard way. It should verify token signatures, and inject the decoded token into the request so that other middlewares can access the user data.

Middlewares must receive in argument the Krypton Authentication URL which can be a relative one (if Krypton Authentication is running on the same server) or an absolute one. It will be able to fetch automatically the public key from Krypton Authentication in order to verify token signatures.

It must not decode the token if it is expired or if its signature is invalid.

If the decryption fails, it should not raise an exception but simply pass the request to the next middleware.

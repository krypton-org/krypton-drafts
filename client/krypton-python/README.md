# krypton-python

Example Python client for GraphQL-Auth-Service.

**NOTE:** Token invalidation has not been tested.  
**NOTE:** The implementation was done quickly and is only an example of what is possible.
In particular the self-contained GraphQL implementation is a bit overkill, and it may be
easier/preferable to directly use strings.

```bash
python example.py
```

```bash
pip install --upgrade pip
pip install .
```

**TODO**

- Django/Flask/... middleware
- Implement all exceptions
- Client serialization (token, cookies)
- KryptonAuthState object?
- Return type, strict mypy configuration

import logging
import uuid

from krypton.auth import KryptonAuthClient, UserToken

client = KryptonAuthClient("https://nusid.net/krypton-auth/auth")
# client = KryptonAuthClient("http://localhost:5000/auth")

username = str(uuid.uuid4())
password = username
email = f"{username}@example.com"

client.register(email, password)
print("Register success")

client.login(email, password)
print(f"Login success: {client.token.user}")

client.update(email=f"{username}-update@example.com")
print(f"Update success: {client.token.user}")

print(f"Test token refreshing")
client.token = UserToken({}, "invalid")

client.update(email=f"{username}-update2@example.com")
print(f"Update success: {client.token.user}")

client.delete(password)
print("Delete success")

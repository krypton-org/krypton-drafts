import logging
import uuid

from krypton.auth import KryptonAuthClient

client = KryptonAuthClient("https://nusid.net/krypton-auth/auth")
# client = KryptonAuthClient("http://localhost:5000/auth")

username = str(uuid.uuid4())
password = username
email = f"{username}@example.com"

client.register(username, email, password)
print("Register success")

client.login(email, password)
print(f"Login success: {client.token.user}")

client.update(username=f"{username}-update")
print(f"Update success: {client.token.user}")

print(f"Test token refreshing")
client.token.token = "zzz"

client.update(username=f"{username}-update-2")
print(f"Update success: {client.token.user}")

client.delete(password)
print("Delete success")

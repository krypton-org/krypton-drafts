import logging
import uuid

from krypton.auth import KryptonAuthClient

logging.basicConfig(level=logging.DEBUG)
client = KryptonAuthClient("https://nusid.net/krypton-auth/auth")

username = str(uuid.uuid4())
password = username
email = f"{username}@example.com"

client.register(username, email, password)
print("Register success")

client.login(email, password)
print(f"Login success: {client.user}")

client.update(username=f"{username}-update")
print(f"Update success: {client.user}")

client.delete(password)
print("Delete success")

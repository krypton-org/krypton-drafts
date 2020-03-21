import uuid

from krypton.auth import KryptonAuthClient

client = KryptonAuthClient("https://nusid.net/krypton-auth/auth")

username = str(uuid.uuid4())
password = username
email = f"{username}@example.com"

client.register(username, email, password)
print("Register success")

user = client.login(email, password)
print(f"Login success: {user}")

client.update(username=f"{username}-update")
print(f"Update success: {user}")

client.delete(password)
print("Delete success")

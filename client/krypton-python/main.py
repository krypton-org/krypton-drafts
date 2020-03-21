from auth import GraphQLAuthClient

client = GraphQLAuthClient("https://nusid.net/graphql-auth-service/auth")

#print(client.register("yourmail", "your@mail.com", "yourpassword"))
print(client.delete("yourpassword"))
print(client.login("your@mail.com", "yourpassword"))
print(client.delete("yourpassword"))
print(client.register("yourmail", "your@mail.com", "yourpassword"))

from .github import Github
from .ping import Ping
from .uptime import Uptime
from .dog import Dog
from .coin import Coin

def setup(client):
    client.add_cog(Github(client))
    client.add_cog(Ping(client))
    client.add_cog(Uptime(client))
    client.add_cog(Dog(client))
    client.add_cog(Coin(client))

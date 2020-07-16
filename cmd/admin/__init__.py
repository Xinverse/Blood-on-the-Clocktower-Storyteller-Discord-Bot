from .ignore import Ignore

def setup(client):
    client.add_cog(Ignore(client))

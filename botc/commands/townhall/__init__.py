from .nominate import Nominate
from .stats import Stats

def setup(client):
    client.add_cog(Nominate(client))
    client.add_cog(Stats(client))

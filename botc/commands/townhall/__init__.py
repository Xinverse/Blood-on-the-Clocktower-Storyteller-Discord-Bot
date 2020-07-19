from .nominate import Nominate
from .stats import Stats
from .townsquare import Townsquare
from .whisper import Whisper

def setup(client):
    client.add_cog(Nominate(client))
    client.add_cog(Stats(client))
    client.add_cog(Townsquare(client))
    client.add_cog(Whisper(client))

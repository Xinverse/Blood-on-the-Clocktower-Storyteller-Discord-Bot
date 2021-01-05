from .join import Join
from .quit import Quit
from .time import Time
from .stats import Stats
from .start import Start
from .notify import Notify
from .wins import Wins

def setup(client):
    client.add_cog(Join(client))
    client.add_cog(Quit(client))
    client.add_cog(Time(client))
    client.add_cog(Stats(client))
    client.add_cog(Start(client))
    client.add_cog(Notify(client))
    client.add_cog(Wins(client))


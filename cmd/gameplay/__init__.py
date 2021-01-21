from .join import Join
from .quit import Quit
from .time import Time
from .stats import Stats
from .start import Start
from .notify import Notify
from .gamestats import Gamestats
from .playerstats import Playerstats
from .top import Top

def setup(client):
    client.add_cog(Join(client))
    client.add_cog(Quit(client))
    client.add_cog(Time(client))
    client.add_cog(Stats(client))
    client.add_cog(Start(client))
    client.add_cog(Notify(client))
    client.add_cog(Gamestats(client))
    client.add_cog(Playerstats(client))
    client.add_cog(Top(client))


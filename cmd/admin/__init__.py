from .ignore import Ignore
from .op import Op
from .deop import Deop
from .fstart import Fstart
from .fjoin import Fjoin
from .fleave import Fleave
from .playtest import Playtest
from .frestart import Frestart

def setup(client):
    client.add_cog(Ignore(client))
    client.add_cog(Op(client))
    client.add_cog(Deop(client))
    client.add_cog(Fstart(client))
    client.add_cog(Fjoin(client))
    client.add_cog(Fleave(client))
    client.add_cog(Playtest(client))
    client.add_cog(Frestart(client))

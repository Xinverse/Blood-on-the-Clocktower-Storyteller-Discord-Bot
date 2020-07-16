from .ignore import Ignore
from .op import Op
from .deop import Deop

def setup(client):
    client.add_cog(Ignore(client))
    client.add_cog(Op(client))
    client.add_cog(Deop(client))

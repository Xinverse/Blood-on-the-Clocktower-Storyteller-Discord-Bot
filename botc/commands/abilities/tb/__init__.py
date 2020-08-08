from .kill import Kill
from .learn import Learn
from .poison import Poison
from .protect import Protect
from .read import Read
from .serve import Serve
from .slay import Slay

def setup(client):
    client.add_cog(Kill(client))
    client.add_cog(Learn(client))
    client.add_cog(Poison(client))
    client.add_cog(Protect(client))
    client.add_cog(Read(client))
    client.add_cog(Serve(client))
    client.add_cog(Slay(client))

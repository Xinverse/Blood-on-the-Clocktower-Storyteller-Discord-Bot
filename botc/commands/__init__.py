def load_abilities():
    """Load all the commands from the "abilities" category"""
    abilities_extension = [
        "kill",
        "learn",
        "poison",
        "protect",
        "read",
        "serve",
        "slay"
    ]
    import globvars
    for extension in abilities_extension:
        globvars.client.load_extension(f"botc.commands.abilities.{extension}")


def load_townhall():
    """Load all the commands from the "townhall" category"""
    townhall_extension = [
        "nominate",
        "townsquare"
    ]
    import globvars
    for extension in townhall_extension:
        globvars.client.load_extension(f"botc.commands.townhall.{extension}")

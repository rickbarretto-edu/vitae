from typing import Annotated

import cyclopts
from cyclopts import Parameter

from vitae.features.bootstrap.usecase import (
    Bootstrap,
    CouldNotResetDatabase,
    DatabaseModelNotFound,
)
from vitae.settings.vitae import Vitae

app = cyclopts.App(name=["bootstrap", "reset", "init"])


@app.default
def bootstrap(
    verbose: Annotated[bool, Parameter(name=["--verbose", "-v"])] = False,
) -> None:
    vitae: Vitae = Vitae.from_toml()

    if vitae.in_production:
        print("This will reset your logs and also your database.")
        print("Insert your user and password before proceeding:\n>>>")
        login: str = input("(Format: 'user:password' )\n>>> ")

        if login != str(vitae.postgres.user):
            msg = "Login doesn't match."
            raise cyclopts.ValidationError(msg)

    try:
        Bootstrap(vitae).new()
    except DatabaseModelNotFound as err:
        print("A required database model was not found.")
        print(f"Tried to import: `{err.path}'")
        print("Please check your code or open an issue on GitHub.")
    except CouldNotResetDatabase as err:
        print(
            "Verify if your database exists or your `vitae.toml` has been set correctly.",
        )
        print()
        print("To manually reset your database, do:")
        print("  $ dropdb <database> -u <user>")
        print("  $ createdb <database> -u <user>")
        if verbose:
            print("Original exception:")
            print(err)

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import jinjax

__all__ = ["templates"]


# =~=~=~=~=~=~= Filters =~=~=~=~=~=~=


def words(text: str) -> list[str]:
    return text.split(" ")


# =~=~=~=~=~=~= Jinja Setup =~=~=~=~=~=~=

env = Environment(
    loader=FileSystemLoader(
        "vitae/features/researchers/templates",
        encoding="utf-8",
    ),
)
env.filters["words"] = words
env.add_extension(jinjax.JinjaX)

templates = Jinja2Templates(directory="vitae/features/researchers/templates")
templates.env = env

catalog = jinjax.Catalog(jinja_env=env)
catalog.add_folder("vitae/features/researchers/templates")

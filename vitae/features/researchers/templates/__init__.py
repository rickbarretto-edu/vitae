import os
import sys

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import jinjax

__all__ = ["templates"]


# =~=~=~=~=~=~= Filters =~=~=~=~=~=~=


def words(text: str) -> list[str]:
    return text.split(" ")


# =~=~=~=~=~=~= Jinja Setup =~=~=~=~=~=~=

# Changes the base-Path when this is compiled by PyIntaller
if getattr(sys, "frozen", False):
    base_path = getattr(sys, "_MEIPASS", ".")
else:
    base_path = os.path.abspath(".")


templates_directory = os.path.join(base_path, "vitae/features/researchers/templates")


env = Environment(
    loader=FileSystemLoader(templates_directory, encoding="utf-8"),
    autoescape=True,
    auto_reload=True,
)
env.filters["words"] = words
env.add_extension(jinjax.JinjaX)

templates = Jinja2Templates(directory=templates_directory)
templates.env = env

catalog = jinjax.Catalog(jinja_env=env)
catalog.add_folder(templates_directory)

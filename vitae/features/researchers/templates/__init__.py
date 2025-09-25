import os

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import jinjax

from vitae.settings.vitae import Vitae

__all__ = ["load_templates"]


# =~=~=~=~=~=~= Filters =~=~=~=~=~=~=


def words(text: str) -> list[str]:
    return text.split(" ")

def initials(name: str) -> str:
    if not name:
        return ""

    def initial(value: str) -> str:
        return value[0].upper()

    if words := [word for word in name.strip().split()]:
        if len(words) == 1:
            return initial(words[0])
        else:
            return initial(words[0]) + initial(words[-1])
    else:
        return ""



# =~=~=~=~=~=~= Jinja Setup =~=~=~=~=~=~=


def load_templates(vitae: Vitae) -> Jinja2Templates:
    """Returns Jinja2 Templates given a global configuration."""

    templates_directory = os.path.join(
        vitae.paths.base, 
        "vitae/features/researchers/templates"
    )

    env = Environment(
        loader=FileSystemLoader(templates_directory, encoding="utf-8"),
        autoescape=True,
        auto_reload=True,
    )
    env.filters["words"] = words
    env.filters["initials"] = initials
    env.add_extension(jinjax.JinjaX)

    templates = Jinja2Templates(directory=templates_directory)
    templates.env = env

    catalog = jinjax.Catalog(jinja_env=env)
    catalog.add_folder(templates_directory)

    return templates
